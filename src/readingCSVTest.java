import org.apache.commons.math3.random.MersenneTwister;
import org.apache.commons.math3.random.RandomGenerator;
import org.deeplearning4j.datasets.fetchers.MnistDataFetcher;
import org.deeplearning4j.datasets.iterator.DataSetIterator;
import org.deeplearning4j.datasets.iterator.impl.ListDataSetIterator;
import org.deeplearning4j.eval.Evaluation;
import org.deeplearning4j.models.classifiers.dbn.DBN;
import org.deeplearning4j.nn.WeightInit;
import org.deeplearning4j.nn.conf.NeuralNetConfiguration;
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

        int nrows=150;
        int ncols=4;
        int nclasses=3;
        INDArray data = Nd4j.ones(nrows,ncols);
        List<String> outcomeTypes = new ArrayList<String>();
        double[][] outcomes = new double[lines.size()][3];



        for(int i = 0; i < nrows; i++) {
            String line = lines.get(i);
            String[] split = line.split(",");

            // turn the 4 numeric values into doubles and add them
            double[] vector = new double[4];
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
                .visibleUnit(RBM.VisibleUnit.GAUSSIAN).regularization(true)
                .l2(2e-2f).dist(Distributions.normal(gen,1.0))
                .activationFunction(Activations.tanh()).iterations(nrows*100)
                .weightInit(WeightInit.DISTRIBUTION)
                .lossFunction(LossFunctions.LossFunction.MCXENT).rng(gen)
                .learningRate(1e-4f).nIn(ncols).nOut(nclasses)
                .build();



        DBN d = new DBN.Builder().configure(conf)
                .hiddenLayerSizes(new int[]{3})
                .build();
        d.getOutputLayer().conf().setWeightInit(WeightInit.ZERO);
        d.getOutputLayer().conf().setActivationFunction(Activations.softMaxRows());
        d.getOutputLayer().conf().setLossFunction(LossFunctions.LossFunction.MCXENT);

        completedData.normalizeZeroMeanZeroUnitVariance();
        completedData.shuffle();
        d.fit(completedData);




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


    }

}