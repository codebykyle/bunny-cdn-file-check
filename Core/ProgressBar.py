
def progressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r", rpad=25):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    padded_prefix = prefix.ljust(rpad)
    print(f'\r{padded_prefix} |{bar}| {percent}% - ({iteration}/{total}) {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()