#include <stdio.h>
#include <stdlib.h>
#include <bcm_host.h>
#include "mailbox.h"
#include "gpu_fft.h"

int runGpuFft(float *input, int points, float* output){
    int ret, mb = mbox_open()
    struct GPU_FFT *fft;

    ret = gpu_fft_prepare(mb, points, GPU_FFT_FWD, 1, &fft);
    if (ret) {
        printf("Failed to prepare GPU FFT, error code: %d\n", ret);
        return ret;
    }

    for (int i = 0; i < points; i++) {
        fft->in[i].re = input[i];  // R
        fft->in[i].im = 0.0f;      // I
    }

    gpu_fft_execute(fft);

    for (int i = 0; i < points; i++) {
        output[i] = fft->out[i].re;  // Get the real part of the output
    }

    // Release GPU resources
    gpu_fft_release(fft);

    return 0;
}