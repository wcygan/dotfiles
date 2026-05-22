function qmd --wraps qmd --description 'Run QMD with stable llama.cpp Metal settings'
    if test (uname) = Darwin
        env GGML_METAL_NO_RESIDENCY=1 GGML_METAL_TENSOR_DISABLE=1 command qmd $argv
    else
        command qmd $argv
    end
end
