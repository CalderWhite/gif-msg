cc_library(
    name = "encoder",
    srcs = ["encoder.cpp"],
    hdrs = ["encoder.h"],
)

cc_library(
    name = "huffman_code",
    hdrs = ["HuffmanCode.h"],
)

cc_binary(
    name = "main",
    srcs = ["main.cpp"],
    deps = [
        ":huffman_code",
        "@boost//:dynamic_bitset",
    ],
)
