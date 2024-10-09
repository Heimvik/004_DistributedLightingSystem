#include <stdio.h>
#include <stdlib.h>
#include <bcm_host.h>
#include "mailbox.h"
#include "gpu_fft.h"

int runGpuFft(float *input, int points, float* output){
    int ret, mb = mbox_open()
    struct GPU_FFT *fft;

    //
}