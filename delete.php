<?php
session_start();
if (!isset($_SESSION['user'])) {
    header("Location: login.php");
    exit;
}
include 'functions.php';
$pdo = pdo_connect();

if (isset($_GET['id'])) {
    $stmt = $pdo->prepare('DELETE FROM contacts WHERE id = ?');
    $stmt->execute([$_GET['id']]);
    header("Location: index.php");
    exit;
} else {
    die("No ID specified!");
}
?>
