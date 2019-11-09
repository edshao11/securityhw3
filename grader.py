"""
NOTE: Grader code will go here. Any modifications here will not be submitted.
"""
def xss_verify(vuln_type, password):
    print(vuln_type, ":", password)

def sql_verify(level, user_pass_list):
    print(level, ":", user_pass_list)

def command_injection_verify(level, flag):
    print(level, ":", flag)


def csrf_verify(level, secret_msg, comments):
    print(level, ":", secret_msg, comments)
