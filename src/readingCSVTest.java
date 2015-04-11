import org.apache.commons.math3.random.MersenneTwister;
import org.apache.commons.math3.random.RandomGenerator;
import org.deeplearning4j.datasets.fetchers.MnistDataFetcher;
import org.deeplearning4j.datasets.iterator.BaseDatasetIterator;
import org.deeplearning4j.datasets.iterator.CSVDataSetIterator;
import org.deeplearning4j.datasets.iterator.DataSetIterator;
import org.deeplearning4j.datasets.iterator.SamplingDataSetIterator;
import org.deeplearning4j.datasets.iterator.impl.ListDataSetIterator;
import org.deeplearning4j.eval.Evaluation;
import org.deeplearning4j.models.classifiers.dbn.DBN;
import org.deeplearning4j.nn.WeightInit;
import org.deeplearning4j.nn.api.NeuralNetwork;
import org.deeplearning4j.nn.conf.NeuralNetConfiguration;
import org.deeplearning4j.optimize.OutputLayerTrainingEvaluator;
import org.nd4j.linalg.api.activation.Activations;
import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.dataset.DataSet;
import org.nd4j.linalg.lossfunctions.LossFunctions;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.nd4j.linalg.factory.Nd4j;
import org.nd4j.linalg.util.Shape;
import org.nd4j.linalg.api.ndarray.INDArray;
import java.io.Serializable;


import org.deeplearning4j.models.featuredetectors.rbm.RBM;
import org.deeplearning4j.distributions.Distributions;



import java.util.Arrays;
import java.io.*;
import java.util.List;
import java.util.ArrayList;

public class readingCSVTest {

    private static Logger log = LoggerFactory.getLogger(readingCSVTest.class);


    public static void main(String[] args) throws Exception {
        RandomGenerator gen = new MersenneTwister(123);

        File f = new File("./Data/merged.csv");
        InputStream fis = new FileInputStream(f);

        List<String> lines = org.apache.commons.io.IOUtils.readLines(fis);

        int nrows=6146;
        int ncols=26;
        int nclasses=5;
        INDArray data = Nd4j.ones(nrows,ncols);
        List<String> outcomeTypes = new ArrayList<String>();
        double[][] outcomes = new double[lines.size()][nclasses];



        for(int i = 0; i < nrows; i++) {
            String line = lines.get(i);
            String[] split = line.split(",");

            // turn the 4 numeric values into doubles and add them
            double[] vector = new double[ncols];
            for(int j = 0; j < ncols; j++)
                vector[j] = Double.parseDouble(split[j]);

            data.putRow(i,Nd4j.create(vector));

            String outcome = split[split.length - 1];
            if(!outcomeTypes.contains(outcome))
                outcomeTypes.add(outcome);

            double[] rowOutcome = new double[nclasses];
            rowOutcome[outcomeTypes.indexOf(outcome)] = 1;
            outcomes[i] = rowOutcome;
        }

        DataSet completedData = new DataSet(data, Nd4j.create(outcomes));

        NeuralNetConfiguration conf = new NeuralNetConfiguration.Builder()
                .hiddenUnit(RBM.HiddenUnit.RECTIFIED).momentum(5e-1f)
                .visibleUnit(RBM.VisibleUnit.GAUSSIAN).regularization(false)
                .l2(2e-2f).dist(Distributions.normal(gen,4.0))
                .activationFunction(Activations.tanh()).iterations(1500)
                .weightInit(WeightInit.DISTRIBUTION)
                .lossFunction(LossFunctions.LossFunction.MCXENT).rng(gen)
                .learningRate(1e-7f).nIn(ncols).nOut(nclasses)
                .build();



        DBN d = new DBN.Builder().configure(conf)
                .hiddenLayerSizes(new int[]{20,15,10})
                .build();
        d.getOutputLayer().conf().setWeightInit(WeightInit.DISTRIBUTION);
        d.getOutputLayer().conf().setActivationFunction(Activations.softMaxRows());
        d.getOutputLayer().conf().setLossFunction(LossFunctions.LossFunction.MCXENT);

        completedData.normalizeZeroMeanZeroUnitVariance();
        completedData.shuffle();


       DataSetIterator dsit = new SamplingDataSetIterator(completedData,5,20000);

        //d.pretrain(dsit,1,0.01f,10);

        int k = 0;
        while(dsit.hasNext()) {
            d.pretrain(dsit.next().getFeatureMatrix(), null);
            k++;
        }

        d.setInput(completedData.getFeatureMatrix());

        for(int i =0; i < 1; i++)
            d.finetune(completedData.getLabels());

        System.out.println("ran " + k + " unsupervised iterations.");
        System.out.println("ran " + 20 + " supervised iterations.");

        /*DataSetIterator iter = new SamplingDataSetIterator(completedData,50,2000);
        while(iter.hasNext())
            d.fit(iter.next());

        iter.reset();
        d.finetune(iter,0.01f );*/



        int[] predict = d.predict(completedData.getFeatureMatrix());
        String[] labels = new String[predict.length];
        double acc=0;
        for(int i = 0; i < predict.length; i++){
                labels[i] = outcomeTypes.get(predict[i]);
                if(outcomes[i][predict[i]]== 1)
                    acc++;
        }
        acc /= predict.length;

        System.out.println("Accuracy: "+acc);
        System.out.println("Predict " + Arrays.toString(labels));

        System.out.println("Model:" + prettyPrint(d));


    }

    static String prettyPrint(DBN d){
        NeuralNetwork[] layers = d.getNeuralNets();
        StringBuffer sb = new StringBuffer();

        INDArray W = d.getInputLayer().getW();
        sb.append("\n\nInput Layer: " +W.rows()+"x"+W.columns()+":\n");
        for(int j = 0; j < W.rows(); j++) {
            sb.append("\n");
            for (int k = 0; k < W.columns(); k++)
                sb.append(W.getDouble(j,k)+ "\t");
        }

        for(int i = 0; i < layers.length; i++) {
            W = layers[i].getW();
            sb.append("\n\nLayer "+i +":"+W.rows()+"x"+W.columns()+":\n");
            for(int j = 0; j < W.rows(); j++) {
                sb.append("\n");
                for (int k = 0; k < W.columns(); k++)
                    sb.append(W.getDouble(j,k)+ "\t");
            }
        }

        W = d.getOutputLayer().getW();
        sb.append("\n\nOutput Layer: " +W.rows()+"x"+W.columns()+":\n");
        for(int j = 0; j < W.rows(); j++) {
            sb.append("\n");
            for (int k = 0; k < W.columns(); k++)
                sb.append(W.getDouble(j,k)+ "\t");
        }

        return sb.toString();
    }

}