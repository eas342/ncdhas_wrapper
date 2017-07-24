NCDHAS Wrapper
-----------------------------------------
A simple python tool for running the NCDHAS ramps-to-slopes pipeline

Instructions
------------------------------------------
* Edit the <a href='run_params/test_params.yaml'>`run_params/test_params.yaml`</a> yaml file and save it as a new file.
* Run the wrapper, often it is easier with the `nohup` command so that you can log out and let `ncdhas` run overnight

	nohup python ncdhas_wrap.py run_params/my_parameters_02.yaml &
