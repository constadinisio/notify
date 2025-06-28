<?php
$host = '18.230.164.213';
$user = 'administrador';
$password = '3167';
$database = 'notify';

$conn = new mysqli($host, $user, $password, $database);
if ($conn->connect_error) {
    die("Error de conexión: " . $conn->connect_error);
}
?>
