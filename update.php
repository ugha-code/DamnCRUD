<?php
session_start();
if (!isset($_SESSION['user'])) {
    header("Location: login.php");
    exit;
}
include 'functions.php';
$pdo = pdo_connect();

if (isset($_GET['id'])) {
    if (!empty($_POST)) {
        $name  = trim($_POST['name']);
        $email = trim($_POST['email']);
        $phone = trim($_POST['phone']);
        $title = trim($_POST['title']);
        $stmt = $pdo->prepare('UPDATE contacts SET name = ?, email = ?, phone = ?, title = ? WHERE id = ?');
        $stmt->execute([$name, $email, $phone, $title, $_GET['id']]);
        header("Location: index.php");
        exit;
    }
    $stmt = $pdo->prepare('SELECT * FROM contacts WHERE id = ?');
    $stmt->execute([$_GET['id']]);
    $contact = $stmt->fetch(PDO::FETCH_ASSOC);
    if (!$contact) {
        die("Contact doesn't exist!");
    }
} else {
    die("No ID specified!");
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <?= style_script() ?>
    <title>Update Contact</title>
</head>
<body>
    <div class="container" style="margin-top:50px">
        <div class="row">
            <div class="col-md-5 col-sm-12 col-xs-12">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Update Contact # <?= htmlspecialchars($contact['id']) ?></h5>
                        <form action="update.php?id=<?= htmlspecialchars($contact['id']) ?>" method="post">
                            <input class="form-control form-control-sm" placeholder="Type name" type="text" name="name" value="<?= htmlspecialchars($contact['name']) ?>" required><br>
                            <input class="form-control form-control-sm" placeholder="Email" type="email" name="email" value="<?= htmlspecialchars($contact['email']) ?>" required><br>
                            <input class="form-control form-control-sm" placeholder="Phone number" type="text" name="phone" value="<?= htmlspecialchars($contact['phone']) ?>" required><br>
                            <input class="form-control form-control-sm" placeholder="Title" type="text" name="title" value="<?= htmlspecialchars($contact['title']) ?>" required><br>
                            <input class="btn btn-primary btn-sm" type="submit" value="Update">
                            <a href="index.php" class="btn btn-warning btn-sm">Cancel</a>
                        </form>
                    </div>
                </div>
            </div>
            <div class="col-md-7 col-sm-12 col-xs-12"></div>
        </div>
    </div>
    <div class="text-center">
        <p class="mt-5 mb-3 text-muted">Your Damn Exercise &copy; 2023</p>
    </div>
</body>
</html>
