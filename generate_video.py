Run python auto_runner.py
Traceback (most recent call last):
  File "/home/runner/work/zero-touch-ai/zero-touch-ai/generate_video.py", line 44, in <module>
    clip.write_videofile(
  File "/opt/hostedtoolcache/Python/3.10.19/x64/lib/python3.10/site-packages/decorator.py", line 234, in fun
    args, kw = fix(args, kw, sig)
  File "/opt/hostedtoolcache/Python/3.10.19/x64/lib/python3.10/site-packages/decorator.py", line 204, in fix
    ba = sig.bind(*args, **kwargs)
  File "/opt/hostedtoolcache/Python/3.10.19/x64/lib/python3.10/inspect.py", line 3186, in bind
    return self._bind(args, kwargs)
  File "/opt/hostedtoolcache/Python/3.10.19/x64/lib/python3.10/inspect.py", line 3175, in _bind
    raise TypeError(
TypeError: got an unexpected keyword argument 'verbose'
Traceback (most recent call last):
  File "/home/runner/work/zero-touch-ai/zero-touch-ai/auto_runner.py", line 22, in <module>
    subprocess.run(["python", "generate_video.py"], check=True)
  File "/opt/hostedtoolcache/Python/3.10.19/x64/lib/python3.10/subprocess.py", line 526, in run
    raise CalledProcessError(retcode, process.args,
subprocess.CalledProcessError: Command '['python', 'generate_video.py']' returned non-zero exit status 1.
Error: Process completed with exit code 1.
