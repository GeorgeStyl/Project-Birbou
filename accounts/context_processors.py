
def auth_status(request):
    if request.user.is_authenticated:  # check if user logged in
        groups = request.user.groups.values_list("name", flat=True)  # get the role of the user
        role = groups[0] if groups else None  # and assign it to a variable "role"  (else None in case user is logged in
                                              # but for some reason not in a group, student or prof). //
                                              # groups[0] because groups will be a query list even though role unique
    else:
        role = None  # if user not logged in - if we want to display different pages to visitors

    return {
        "is_logged_in": request.user.is_authenticated,
        "user_role": role,  # global variable to be used to decide role: user_role
    }
