    
def retry(times, exceptions):
    """
    Retry Decorator
    Retries the wrapped function/method `times` times if the exceptions listed
    in ``exceptions`` are thrown
    :param times: The number of times to repeat the wrapped function/method
    :type times: Int
    :param Exceptions: Lists of exceptions that trigger a retry attempt
    :type Exceptions: Tuple of Exceptions
    """
    def decorator(func):
        def newfn(*args, **kwargs):
            attempt = 0
            while attempt < times:
                print attempt,args,kwargs
                if attempt == 1:
                  print "changing resturi for attempt 1"
                  converttolist = list(args)

                  converttolist[5] = '/mgmt/tm/sys/software/image'
                  args  = tuple(converttolist)
                  print args
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    print(
                          'Exception thrown when attempting to run %s, attempt '
                        '%d of %d' % (func, attempt, times)
                        )
                    attempt += 1
            return func(*args, **kwargs)
        return newfn
    return decorator

