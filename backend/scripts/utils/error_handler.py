def safe_exectue(function,*args):

    try:
        return function(*args)
    
    except Exception as e:
        print("System Error:",e)

        return "The system encountered an issue while processing your rquest."