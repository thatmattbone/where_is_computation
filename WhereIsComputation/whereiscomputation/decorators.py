import markdown

def update_with_func_info(original_func):
    """
    Run the view function and update its context with:

      docstring: the docstring of the view function
      code_url: the url of the function (including the line number anchor) on github
    """
    def new_func(*args, **kwargs):

        context = original_func(*args[1:], **kwargs)  # HACK the args[1:] is because of the implied root_factory arg
        
        base_url = 'https://github.com/thatmattbone/where_is_computation/blob/master/WhereIsComputation/whereiscomputation/views.py#L{line_no}'

        docstring = original_func.__doc__
        docstring = "\n".join([line.strip() for line in docstring.split("\n")])
        docstring = markdown.markdown(docstring)
    
        context.update({'docstring': docstring,
                        'code_url': base_url.format(line_no=original_func.__code__.co_firstlineno)})

        return context

    new_func.__name__ = original_func.__name__
    new_func.__doc__ = original_func.__doc__
    new_func.__dict__.update(original_func.__dict__)

    return new_func
