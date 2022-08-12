# Authentication App

#### All the links are appended by `{domain-name}/auth`

### `login-with-google/`

> This will Sign In with Google and send back *Access and Refresh Tokens*
> > If the user is not registered in the system, it will create a new user and send back *Access and Refresh Tokens*

### `oauth2callback/`

> This is a call back which is used by our API backend it generates authentication URL of Google Account

### `sign-in/`

> Sign with Email and Password and Sends back Credentials to the client

### `sign-up/`

> This will Sign Up with Email and Password and Sends Ok Message to the client

### `token/`

> Takes User Credentials and Sends back Access and Refresh Tokens to the client

### `refresh-token/`

> Takes Refresh Token and Sends back Access and Refresh Tokens to the client

#### All the views are protected by `JWT` to access any view , you need to send `Authorization` header with `Bearer` and `JWT` token, or you can add @permission_classes([AllowAny]) to the view in function based view or in class based view add `permissionclasses=[AllowAny]` to the view


