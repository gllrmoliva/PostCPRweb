student = { 'email':'student@student.com',
            'password':'1234'
}

tutor = { 'email':'tutor@tutor.com',
            'password':'5678'
}


def studentInDB(email, password):
    if (student['email'] == email) and (student['password'] == password):
        return True
    else:
        return False

def tutorInDB(email, password):
    if (tutor['email'] == email) and (tutor['password'] == password):
        return True
    else:
        return False