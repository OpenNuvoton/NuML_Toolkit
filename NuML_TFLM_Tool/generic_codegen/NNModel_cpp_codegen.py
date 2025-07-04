import sys
import tflite
import os
from jinja2 import Environment, FileSystemLoader

CUSTOM_OPCODE2TFLMFUN = {
    'CIRCULAR_BUFFER': 'AddCircularBuffer',
    'ethos-u': 'AddEthosU',
    'SignalDelay': 'AddDelay',
    'TFLite_Detection_PostProcess': 'AddDetectionPostprocess',
    'SignalEnergy': 'AddEnergy',
    'SignalFftAutoScale': 'AddFftAutoScale',
    'SignalFilterBank': 'AddFilterBank',
    'SignalFilterBankLog': 'AddFilterBankLog',
    'SignalFilterBankSquareRoot': 'AddFilterBankSquareRoot',
    'SignalFilterBankSpectralSubtraction': 'AddFilterBankSpectralSubtraction',
    'SignalFramer': 'AddFramer',
    'SignalIrfft': 'AddIrfft',
    'SignalOverlapAdd': 'AddOverlapAdd',
    'SignalPCAN': 'AddPCAN',
    'SignalRfft': 'AddRfft',
    'SignalStacker': 'AddStacker',
    'SignalWindow': 'AddWindow'
}

BUILTIN_OPCODE2TFLMFUN = {
    0: 'AddAdd',
    1: 'AddAveragePool2D',
    2: 'AddConcatenation',
    3: 'AddConv2D',
    4: 'AddDepthwiseConv2D',
    5: 'AddDepthToSpace',
    6: 'AddDequantize',
    7: 'AddEmbeddingLookup',
    8: 'AddFloor',
    9: 'AddFullyConnected',
    10: None,                   #'HASHTABLE_LOOKUP',
    11: 'AddL2Normalization',
    12: 'AddL2Pool2D',
    13: None,                   #'LOCAL_RESPONSE_NORMALIZATION',
    14: 'AddLogistic',
    15: None,                   #'LSH_PROJECTION',
    16: None,                   #'LSTM',
    17: 'AddMaxPool2D',
    18: 'AddMul',
    19: 'AddRelu',
    20: None,                   #'RELU_N1_TO_1',
    21: 'AddRelu6',
    22: 'AddReshape',
    23: 'AddResizeBilinear',
    24: None,                   #'RNN',
    25: 'AddSoftmax',
    26: 'AddSpaceToDepth',
    27: 'AddSvdf',
    28: 'AddTanh',
    29: None,                   #'CONCAT_EMBEDDINGS',
    30: None,                   #'SKIP_GRAM',
    31: None,                   #'CALL',
    32: None,                   #'CUSTOM' using CUSTOM_OPCODE2TFLMFUN
    33: None,                   #'EMBEDDING_LOOKUP_SPARSE',
    34: 'AddPad',
    35: None,                   #'UNIDIRECTIONAL_SEQUENCE_RNN',
    36: 'AddGather',
    37: 'AddBatchToSpaceNd',
    38: 'AddSpaceToBatchNd',
    39: 'AddTranspose',
    40: 'AddMean',
    41: 'AddSub',
    42: 'AddDiv',
    43: 'AddSqueeze',
    44: 'AddUnidirectionalSequenceLSTM',
    45: 'AddStridedSlice',
    46: None,                   #'BIDIRECTIONAL_SEQUENCE_RNN',
    47: 'AddExp',
    48: None,                   #'TOPK_V2',
    49: 'AddSplit',
    50: 'AddLogSoftmax',
    51: None,                   #'DELEGATE',
    52: None,                   #'BIDIRECTIONAL_SEQUENCE_LSTM',
    53: 'AddCast',
    54: 'AddPrelu',
    55: 'AddMaximum',
    56: 'AddArgMax',
    57: 'AddMinimum',
    58: 'AddLess',
    59: 'AddNeg',
    60: 'AddPadV2',
    61: 'AddGreater',
    62: 'AddGreaterEqual',
    63: 'AddLessEqual',
    64: None,                   #'SELECT',
    65: 'AddSlice',
    66: 'AddSin',
    67: 'AddTransposeConv',
    68: None,                   #'SPARSE_TO_DENSE',
    69: None,                   #'TILE',
    70: 'AddExpandDims',
    71: 'AddEqual',
    72: 'AddNotEqual',
    73: 'AddLog',
    74: 'AddSum',
    75: 'AddSqrt',
    76: 'AddRsqrt',
    77: 'AddShape',
    78: None,                   #'POW',
    79: 'AddArgMin',
    80: None,                   #'FAKE_QUANT',
    81: None,                   #'REDUCE_PROD',
    82: 'AddReduceMax',
    83: 'AddPack',
    84: 'AddLogicalOr',
    85: None,                   #'ONE_HOT',
    86: 'AddLogicalAnd',
    87: 'AddLogicalNot',
    88: 'AddUnpack',
    89: 'AddReduceMin',
    90: 'AddFloorDiv',
    91: None,                   #'REDUCE_ANY',
    92: 'AddSquare',
    93: 'AddZerosLike',
    94: 'AddFill',
    95: 'AddFloorMod',
    96: None,                   #'RANGE',
    97: 'AddResizeNearestNeighbor',
    98: 'AddLeakyRelu',
    99: 'AddSquaredDifference',
    100: 'AddMirrorPad',
    101: 'AddAbs',
    102: 'AddSplitV',
    103: None,                  #'UNIQUE',
    104: 'AddCeil',
    105: None,                  #'REVERSE_V2',
    106: 'AddAddN',
    107: 'AddGatherNd',
    108: 'AddCos',
    109: None,                  #'WHERE',
    110: None,                  #'RANK',
    111: 'AddElu',
    112: None,                  #'REVERSE_SEQUENCE',
    113: None,                  #'MATRIX_DIAG',
    114: 'AddQuantize',
    115: None,                  #'MATRIX_SET_DIAG',
    116: 'AddRound',
    117: 'AddHardSwish',
    118: 'AddIf',
    119: 'AddWhile',
    120: None,                  #'NON_MAX_SUPPRESSION_V4',
    121: None,                  #'NON_MAX_SUPPRESSION_V5',
    122: None,                  #'SCATTER_ND',
    123: 'AddSelectV2',
    124: None,                  #'DENSIFY',
    125: None,                  #'SEGMENT_SUM',
    126: 'AddBatchMatMul',
    127: None,                  #'PLACEHOLDER_FOR_GREATER_OP_CODES',
    128: 'AddCumSum',
    129: 'AddCallOnce',
    130: 'AddBroadcastTo',
    131: None,                  #'RFFT2D',
    132: None,                  #'CONV_3D',
    133: None,                  #'IMAG',
    134: None,                  #'REAL',
    135: None,                  #'COMPLEX_ABS',
    136: None,                  #'HASHTABLE',
    137: None,                  #'HASHTABLE_FIND',
    138: None,                  #'HASHTABLE_IMPORT',
    139: None,                  #'HASHTABLE_SIZE',
    140: None,                  #'REDUCE_ALL',
    141: None,                  #'CONV_3D_TRANSPOSE',
    142: 'AddVarHandle',
    143: 'AddReadVariable',
    144: 'AddAssignVariable',
    145: 'AddBroadcastArgs',
    146: None,                  #'RANDOM_STANDARD_NORMAL',
    147: None,                  #'BUCKETIZE',
    148: None,                  #'RANDOM_UNIFORM',
    149: None,                  #'MULTINOMIAL',
    150: None,                  #'GELU',
    151: None,                  #'DYNAMIC_UPDATE_SLICE',
    152: None,                  #'RELU_0_TO_1',
    153: None,                  #'UNSORTED_SEGMENT_PROD',
    154: None,                  #'UNSORTED_SEGMENT_MAX',
    155: None,                  #'UNSORTED_SEGMENT_SUM',
    156: None,                  #'ATAN2',
    157: None,                  #'UNSORTED_SEGMENT_MIN',
    158: None,                  #'SIGN',
}

def GetTflmBuiltinOPFunciton(opcode):
    if opcode in BUILTIN_OPCODE2TFLMFUN:
        return BUILTIN_OPCODE2TFLMFUN[opcode]
    else:
        raise ValueError("Unknown builtin opcode %d, should be a custom operator." % opcode)

def GetTflmCustomOPFunciton(opcode):
    if opcode in CUSTOM_OPCODE2TFLMFUN:
        return CUSTOM_OPCODE2TFLMFUN[opcode]
    else:
        raise ValueError("Unknown custom opcode %s." % opcode)


def add_operators_section(model_file):
    f = open(model_file, 'rb')
    buf = f.read()
    model = tflite.Model.GetRootAsModel(buf, 0)
    subgraph = model.Subgraphs(0)
    num_operators = subgraph.OperatorsLength()

    builtin_opcode_list  = []
    custom_opcode_list  = []
    all_op_list = []

    for op_index in range(num_operators):
        operator = subgraph.Operators(op_index)
        opcode = model.OperatorCodes(operator.OpcodeIndex())
        opcode_id = opcode.BuiltinCode()

        if opcode_id != tflite.BuiltinOperator.CUSTOM :
            if opcode_id not in builtin_opcode_list:
                builtin_opcode_list.append(opcode_id)
        else :
            custom_opcode = opcode.CustomCode().decode("utf-8") 
            if custom_opcode not in custom_opcode_list:
                custom_opcode_list.append(custom_opcode)

    for op_code in builtin_opcode_list:
        operator_add_function = GetTflmBuiltinOPFunciton(op_code)

        if operator_add_function == None:
            print(f"Unknown builtin opcode {op_code}, should be a custom operator.")
            raise ValueError("Not supported operator by TFLM")

        all_op_list.append(operator_add_function)

    for op_code in custom_opcode_list:
        operator_add_function = GetTflmCustomOPFunciton(op_code)

        if operator_add_function == None:
            print(f"Unknown custom opcode {op_code}.")
            raise ValueError("Not supported operator by TFLM")

        all_op_list.append(operator_add_function)

    f.close()
    return all_op_list

class NNModelCppCodegen:
    def code_gen(self, NNModel_cpp_file, template_file, model_file):
        tmpl_dirname = os.path.dirname(template_file)
        tmpl_basename = os.path.basename(template_file)
        env =  Environment(loader=FileSystemLoader(tmpl_dirname), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(tmpl_basename)
        operator_list = add_operators_section(model_file)
        output = template.render(operators = operator_list)
        NNModel_cpp_file.write(output)
