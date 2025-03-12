<?php
session_start();
if (!isset($_SESSION['user'])) {
    header("Location: login.php");
    exit;
}
include "functions.php";
$error = "";
if (isset($_FILES['image'])) {
    $file_name = $_FILES['image']['name'];
    $file_tmp  = $_FILES['image']['tmp_name'];
    $tmp = explode('.', $file_name);
    $file_ext = strtolower(end($tmp));
    $extensions = array("jpeg", "jpg");
    
    if (!in_array($file_ext, $extensions)) {
       $error = "Ekstensi tidak diijinkan. Hanya menerima file JPG/JPEG";
    }
    if (empty($error)) {
       move_uploaded_file($file_tmp, "image/profile.jpg");
       header("Location: profil.php");
       exit;
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <?= style_script() ?>
    <title>Profil</title>
</head>
<body>
    <div class="container">
        <h2>Profil</h2>
        <div class="row">
            <div class="col">
                <a class="btn btn-primary" href="index.php">Dashboard</a>
                <div class="action float-right">
                    <a class="btn btn-danger" href="logout.php">Sign out</a> 
                </div>                  
            </div>
        </div>
        <br><br>
        <div class="row">
            <div class="col-md-4 order-md-2 mb-4">
                <ul class="list-group mb-3">
                    <li class="list-group-item d-flex justify-content-between lh-condensed">
                        <div>
                            <img src="image/profile.jpg" style="width:100%" alt="Profile Image"/>
                        </div>
                    </li>
                </ul>
                <form class="card p-2" action="profil.php" method="POST" enctype="multipart/form-data">
                    <div class="input-group">
                        <input class="form-control" type="file" id="formFile" name="image">
                        <div class="input-group-append">                    
                            <button type="submit" class="btn btn-secondary">Change</button>
                        </div>
                    </div>
                </form>
                <small>* JPG/JPEG only</small>
                <?= $error; ?>
            </div>
            <div class="col-md-8 order-md-1">
                <form class="needs-validation" novalidate>
                    <div class="mb-3">
                        <label for="username">Username</label>
                        <input type="text" class="form-control" id="username" value="<?= htmlspecialchars($_SESSION['user']); ?>" disabled>
                    </div>
                    <div class="mb-3">
                        <label for="password">Password</label>
                        <input type="password" class="form-control" id="password" value="*********" disabled>
                    </div>
                </form>
            </div>
        </div>
    </div>
    <div class="text-center">
        <p class="mt-5 mb-3 text-muted">Your Damn Exercise &copy; 2023</p>
    </div>
</body>
</html>
