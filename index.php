<?php
session_start();
if (!isset($_SESSION['user'])) {
    header("Location: login.php");
    exit;
}
include "functions.php";
$pdo = pdo_connect();
$stmt = $pdo->prepare('SELECT * FROM contacts');
$stmt->execute();
$contacts = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <?= style_script() ?>
    <script>
        $(document).ready(function() {
            $('#employee').DataTable();
        });
    </script>
    <title>Dashboard</title>
</head>
<body>
    <div class="container">
        <h2>Howdy, damn <?= htmlspecialchars($_SESSION['user']); ?>!</h2>
        <?php include "menu.php"; ?>
        <div class="row">
            <div class="col">
                <table class="table table-striped" id="employee">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Phone</th>
                            <th>Title</th>
                            <th>Created</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($contacts as $contact) : ?>
                            <tr>
                                <td><?= htmlspecialchars($contact['id']) ?></td>
                                <td><?= htmlspecialchars($contact['name']) ?></td>
                                <td><?= htmlspecialchars($contact['email']) ?></td>
                                <td><?= htmlspecialchars($contact['phone']) ?></td>
                                <td><?= htmlspecialchars($contact['title']) ?></td>
                                <td><?= htmlspecialchars($contact['created']) ?></td>
                                <td class="actions">
                                    <a class="btn btn-sm btn-outline btn-success" href="update.php?id=<?= htmlspecialchars($contact['id']) ?>">edit</a>
                                    <a class="btn btn-sm btn-outline btn-danger" href="delete.php?id=<?= htmlspecialchars($contact['id']) ?>" onclick="return confirm('Damn, what r u doin\'? Are you sure?');">delete</a>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                    <tfoot>
                        <tr>
                            <th>#</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Phone</th>
                            <th>Title</th>
                            <th>Created</th>
                            <th></th>
                        </tr>
                    </tfoot>
                </table>
            </div>
        </div>
    </div>
    <div class="text-center">
        <p class="mt-5 mb-3 text-muted">Your Damn Exercise &copy; 2023</p>
    </div>
</body>
</html>
