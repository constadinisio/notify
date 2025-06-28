<?php
// index.php
// Conexión y manejo de acciones
require 'conexion.php';

// Eliminar un evento
if (isset($_GET['delete'])) {
  $id = intval($_GET['delete']);
  $conn->query("DELETE FROM eventos WHERE id = $id");
  header('Location: index.php');
  exit;
}

// Borrar todo
if (isset($_POST['clear_all'])) {
  $conn->query("DELETE FROM logs");
  header('Location: index.php');
  exit;
}

// Contadores
$today = date('Y-m-d');
$resDaily = $conn->query("SELECT COUNT(*) AS cnt FROM eventos WHERE fecha = '$today'");
$daily = $resDaily->fetch_assoc()['cnt'];

$res28 = $conn->query("SELECT COUNT(*) AS cnt FROM eventos WHERE fecha >= DATE_SUB('$today', INTERVAL 28 DAY)");
$last28 = $res28->fetch_assoc()['cnt'];

$resTotal = $conn->query("SELECT COUNT(*) AS cnt FROM eventos");
$total = $resTotal->fetch_assoc()['cnt'];

// Logs recientes
$resLogs = $conn->query("SELECT id, fecha, hora, fuera_de_horario FROM eventos ORDER BY fecha DESC, hora DESC LIMIT 20");
?>
<!DOCTYPE html>
<html lang="es">

<head>
  <meta charset="UTF-8">
  <title>Notify Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    div {
      font-family: 'Poppins';
    }

    img {
      width: 40px;
      height: 40px;
    }
  </style>
</head>

<body class="bg-gray-100 font-sans">
  <div class="flex">
    <!-- Sidebar -->
    <aside class="w-64 bg-gray-800 min-h-screen text-white">
      <div class="p-6 text-3xl font-bold border-b border-gray-700">
        <a href="#" class="flex items-center">
          <img src="./images/notify.png" class="mr-2">
          Notify
        </a>
      </div>
      <nav class="mt-6">
        <a href="index.php" class="flex items-center py-3 px-6 bg-gray-700 hover:bg-gray-600">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M13 5v6h6" />
          </svg>
          Dashboard
        </a>
      </nav>
    </aside>

    <!-- Main content -->
    <main class="flex-1 p-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <!-- Daily Notifications -->
        <div class="bg-white p-6 rounded-lg shadow">
          <p class="text-gray-600 uppercase">Daily Notifications</p>
          <p class="text-4xl font-semibold text-green-500 mt-2"><?php echo $daily; ?></p>
          <div class="h-1 bg-green-300 mt-4" style="width: <?php echo min(100, ($daily / max(1, $total)) * 100); ?>%"></div>
        </div>
        <!-- Last 28 Days -->
        <div class="bg-white p-6 rounded-lg shadow">
          <p class="text-gray-600 uppercase">Last 28 Days</p>
          <p class="text-4xl font-semibold text-purple-500 mt-2"><?php echo $last28; ?></p>
          <div class="h-1 bg-purple-300 mt-4" style="width: <?php echo min(100, ($last28 / max(1, $total)) * 100); ?>%"></div>
        </div>
        <!-- Total Requests -->
        <div class="bg-white p-6 rounded-lg shadow">
          <p class="text-gray-600 uppercase">Total Requests</p>
          <p class="text-4xl font-semibold text-blue-500 mt-2"><?php echo $total; ?></p>
          <div class="h-1 bg-blue-300 mt-4" style="width: 100%;"></div>
        </div>
      </div>

      <!-- Logs section -->
      <div class="bg-white rounded-lg shadow">
        <div class="flex justify-between items-center p-4 border-b">
          <h2 class="text-xl font-semibold">Recent Notifications</h2>
          <form method="post" action="index.php">
            <button name="clear_all" class="bg-indigo-500 hover:bg-indigo-600 text-white px-4 py-2 rounded">Clear All Notifications</button>
          </form>
        </div>
        <div class="divide-y">
          <?php while ($row = $resLogs->fetch_assoc()): ?>
            <?php $isOut = (int)$row['fuera_de_horario'] === 1; ?>
            <div class="flex items-center justify-between p-4 hover:bg-gray-50">
              <div class="flex items-center">
                <div class="h-10 w-10 rounded-full bg-<?php echo $isOut ? 'green' : 'red'; ?>-400 flex items-center justify-center text-white">
                  <?php echo $isOut ? '✅' : '❗'; ?>
                </div>
                <div class="ml-4">
                  <p class="text-2x1 text-gray-500">
                    <?php
                    echo $row['fuera_de_horario'] == 0
                      ? " Movimiento fuera de Horario"
                      : " Movimiento dentro de Horario";
                    ?>
                  </p>

                </div>
              </div>
              <div class="flex items-center space-x-4">
                <p class="text-sm text-gray-500"><?php echo date('M j, Y, g:i a', strtotime($row['fecha'] . ' ' . $row['hora'])); ?></p>
                <a href="?delete=<?php echo $row['id']; ?>" class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded">Delete</a>
              </div>
            </div>
          <?php endwhile; ?>
        </div>
      </div>
    </main>
  </div>
</body>

</html>