import org.apache.commons.math3.random.MersenneTwister;
import org.apache.commons.math3.random.RandomGenerator;
import org.deeplearning4j.datasets.iterator.DataSetIterator;
import org.deeplearning4j.datasets.iterator.SamplingDataSetIterator;
import org.deeplearning4j.distributions.Distributions;
import org.deeplearning4j.models.classifiers.dbn.DBN;
import org.deeplearning4j.models.featuredetectors.rbm.RBM;
import org.deeplearning4j.nn.WeightInit;
import org.deeplearning4j.nn.api.NeuralNetwork;
import org.deeplearning4j.nn.conf.NeuralNetConfiguration;
import org.nd4j.linalg.api.activation.Activations;
import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.dataset.DataSet;
import org.nd4j.linalg.factory.Nd4j;
import org.nd4j.linalg.lossfunctions.LossFunctions;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class NNImporter {

    private static Logger log = LoggerFactory.getLogger(NNImporter.class);


    public static void main(String[] args) throws Exception {
        RandomGenerator gen = new MersenneTwister(123);

        String NNFile = args[0];
        String DataFile = args[1];

    }

    public static DataSet parseData(String NNFile) {
        File f = new File(NNFile);
        InputStream fis = null;
        try {
            fis = new FileInputStream(f);
        } catch (java.io.FileNotFoundException e) {
            System.err.println("Error: File " + NNFile + " does not exist, or wrong path was provided.\n");
            System.exit(1);
        }
        List<String> lines = null;
        try {
            lines = org.apache.commons.io.IOUtils.readLines(fis);
        } catch (java.io.IOException e) {
            System.err.println("Error: Unable to parse passed CSV file: " + NNFile);
            System.exit(1);
        }
        int nrows = 6146;
        int ncols = 26;
        int nclasses = 5;
        INDArray data = Nd4j.ones(nrows, ncols);
        List<String> outcomeTypes = new ArrayList<String>();
        double[][] outcomes = new double[lines.size()][nclasses];


        for (int i = 0; i < nrows; i++) {
            String line = lines.get(i);
            String[] split = line.split(",");

            // turn the 4 numeric values into doubles and add them
            double[] vector = new double[ncols];
            for (int j = 0; j < ncols; j++)
                vector[j] = Double.parseDouble(split[j]);

            data.putRow(i, Nd4j.create(vector));

            String outcome = split[split.length - 1];
            if (!outcomeTypes.contains(outcome))
                outcomeTypes.add(outcome);

            double[] rowOutcome = new double[nclasses];
            rowOutcome[outcomeTypes.indexOf(outcome)] = 1;
            outcomes[i] = rowOutcome;
        }

        return new DataSet(data, Nd4j.create(outcomes));
    }

    public NeuralNetwork

        NeuralNetConfiguration conf = new NeuralNetConfiguration.Builder()
                .hiddenUnit(RBM.HiddenUnit.RECTIFIED).momentum(5e-1f)
                .visibleUnit(RBM.VisibleUnit.GAUSSIAN).regularization(false)
                .l2(2e-2f).dist(Distributions.normal(gen, 4.0))
                .activationFunction(Activations.tanh()).iterations(1500)
                .weightInit(WeightInit.DISTRIBUTION)
                .lossFunction(LossFunctions.LossFunction.MCXENT).rng(gen)
                .learningRate(1e-7f).nIn(ncols).nOut(nclasses)
                .build();


        DBN d = new DBN.Builder().configure(conf)
                .hiddenLayerSizes(new int[]{20, 15, 10})
                .build();
        d.getOutputLayer().conf().setWeightInit(WeightInit.DISTRIBUTION);
        d.getOutputLayer().conf().setActivationFunction(Activations.softMaxRows());
        d.getOutputLayer().conf().setLossFunction(LossFunctions.LossFunction.MCXENT);

        completedData.normalizeZeroMeanZeroUnitVariance();
        completedData.shuffle();


        DataSetIterator dsit = new SamplingDataSetIterator(completedData, 5, 20000);

        //d.pretrain(dsit,1,0.01f,10);

        int k = 0;
        while (dsit.hasNext()) {
            d.pretrain(dsit.next().getFeatureMatrix(), null);
            k++;
        }

        d.setInput(completedData.getFeatureMatrix());

        for (int i = 0; i < 1; i++)
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
        double acc = 0;
        for (int i = 0; i < predict.length; i++) {
            labels[i] = outcomeTypes.get(predict[i]);
            if (outcomes[i][predict[i]] == 1)
                acc++;
        }
        acc /= predict.length;

        System.out.println("Accuracy: " + acc);
        System.out.println("Predict " + Arrays.toString(labels));

        System.out.println("Model:" + prettyPrint(d));


    }

    static String prettyPrint(DBN d) {
        NeuralNetwork[] layers = d.getNeuralNets();
        StringBuffer sb = new StringBuffer();

        INDArray W = d.getInputLayer().getW();
        sb.append("\n\nInput Layer: " + W.rows() + "x" + W.columns() + ":\n");
        for (int j = 0; j < W.rows(); j++) {
            sb.append("\n");
            for (int k = 0; k < W.columns(); k++)
                sb.append(W.getDouble(j, k) + "\t");
        }

        for (int i = 0; i < layers.length; i++) {
            W = layers[i].getW();
            sb.append("\n\nLayer " + i + ":" + W.rows() + "x" + W.columns() + ":\n");
            for (int j = 0; j < W.rows(); j++) {
                sb.append("\n");
                for (int k = 0; k < W.columns(); k++)
                    sb.append(W.getDouble(j, k) + "\t");
            }
        }

        W = d.getOutputLayer().getW();
        sb.append("\n\nOutput Layer: " + W.rows() + "x" + W.columns() + ":\n");
        for (int j = 0; j < W.rows(); j++) {
            sb.append("\n");
            for (int k = 0; k < W.columns(); k++)
                sb.append(W.getDouble(j, k) + "\t");
        }

        return sb.toString();
    }

}