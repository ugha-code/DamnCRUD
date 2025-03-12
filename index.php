<?php
session_start();
include "functions.php";
if (!isset($_SESSION['user'])) {
    header("Location: login.php");
    exit;
}
$pdo = pdo_connect();
$stmt = $pdo->query("SELECT * FROM contacts");
$contacts = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dashboard</title>
    <?= style_script() ?>
</head>
<body>
    <h2>Welcome, <?= htmlspecialchars($_SESSION['user']); ?>!</h2>
    <!-- Elemen dengan id "employee" untuk memudahkan pengecekan test -->
    <div id="employee">
        <table class="table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Name</th>
                    <th>Email</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($contacts as $contact): ?>
                <tr>
                    <td><?= $contact['id'] ?></td>
                    <td><?= htmlspecialchars($contact['name']) ?></td>
                    <td><?= htmlspecialchars($contact['email']) ?></td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
    <!-- Link untuk membuat kontak baru -->
    <a href="create.php">Add New Contact</a>
</body>
</html>
