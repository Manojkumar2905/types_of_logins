try:
    from apis.client_admin.create_user import *
except Exception as e:
    print(f"Error in apis.client_admin.create_user : {e}")
    
try:
    from apis.client_admin.register_user_with_face import *
except Exception as e:
    print(f"Error in apis.client_admin.register_user_with_face : {e}")

try:
    from apis.client_admin.login_with_face import *
except Exception as e:
    print(f"Error in apis.client_admin.login_with_face : {e}")