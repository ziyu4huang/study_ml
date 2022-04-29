import ray 

# Normal Ray code follows
@ray.remote
def do_work(x):
    return x ** x

rs = do_work.remote(2)
print("remote do_work() return, refs",  rs)
print("remote do_work() return, value",  ray.get(rs))

