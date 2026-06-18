# Overview
While developing the recipe and electrolyte composition solver, new errors began appearing when using non-integer volume amounts. At first this seemed to possibly be a hardware limitation, but reviewing the technical documentation for the machine indicates that the system should be capable of 0.5 uL increments. 

# Previous attempts at resolving the issue
1. The use of integers is currently hard-coded into the sartorius interface in a number of places. If these are removed, there is a typing error raised: the system expects integers for the volume parameter, as specified in SartoriusCtrl.srv (located in battery_lab_custom_msg). The ```int32``` spec can be changed to float32 (which will require rebuilding the battery_lab_custom_msg package), but this causes an anonymous error to be thrown when this command is passed to the pipetter. 
