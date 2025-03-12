<?php
session_start();
if (!isset($_SESSION['user'])) {
    header("Location: login.php");
    exit;
}
include 'functions.php';
$pdo = pdo_connect();

if (!empty($_POST)) {
    $name  = trim($_POST['name']);
    $email = trim($_POST['email']);
    $phone = trim($_POST['phone']);
    $title = trim($_POST['title']);
    $created = date('Y-m-d H:i:s');
    // Memasukkan data dengan menyebutkan kolom secara eksplisit
    $stmt = $pdo->prepare('INSERT INTO contacts (name, email, phone, title, created) VALUES (?, ?, ?, ?, ?)');
    $stmt->execute([$name, $email, $phone, $title, $created]);
    header("Location: index.php");
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <?= style_script() ?>
    <title>Add New Contact</title>
</head>
<body>
    <div class="container" style="margin-top:50px">
        <div class="row">
            <div class="col-md-5 col-sm-12 col-xs-12">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Add New Contact</h5>
                        <form action="create.php" method="post">
                            <input class="form-control form-control-sm" placeholder="Type name" type="text" name="name" required><br>
                            <input class="form-control form-control-sm" placeholder="Email" type="email" name="email" required><br>
                            <input class="form-control form-control-sm" placeholder="Phone number" type="text" name="phone" required><br>
                            <input class="form-control form-control-sm" placeholder="Title" type="text" name="title" required><br>
                            <input class="btn btn-primary btn-sm" type="submit" value="Save">
                            <a href="index.php" class="btn btn-warning btn-sm">Cancel</a>
                        </form>
                    </div>
                    <div class="col-md-7 col-sm-12 col-xs-12"></div>
                </div>
            </div>
        </div>
    </div>
    <div class="text-center">
        <p class="mt-5 mb-3 text-muted">Your Damn Exercise &copy; 2023</p>
    </div>
</body>
</html>
