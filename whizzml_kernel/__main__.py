from ipykernel.kernelapp import IPKernelApp
from . import WhizzMLKernel

IPKernelApp.launch_instance(kernel_class=WhizzMLKernel)
