package gov.nist.eee.object;

import gov.nist.eee.object.tree.Tree;
import nz.sodium.CellSink;

/**
 * A Model represents the network of inputs and calculations that result in the E3 economic analysis.
 */
public record Model(Tree<String, CellSink<Double>> doubleInputs, Tree<String, CellSink<Integer>> intInputs) {

}
