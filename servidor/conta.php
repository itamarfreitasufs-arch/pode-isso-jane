<?php
// Pode isso, Jane? Contador de usos.
// Grava só: dia, tipo de evento, perfil e código da ficha. Não grava IP, navegador, hora,
// cookie nem nada do que a pessoa escreve. Os totais ficam em contagem/AAAA-MM.json.
header('Cache-Control: no-store');
header('Content-Type: text/plain; charset=utf-8');
// GET: devolve só o total de visitas, para o número discreto no rodapé do app.
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
  $total = 0;
  foreach (glob(__DIR__ . '/contagem/*.json') ?: [] as $arq) {
    $d = json_decode((string) @file_get_contents($arq), true);
    if (is_array($d)) foreach ($d as $chaves) $total += (int) ($chaves['visita'] ?? 0);
  }
  echo $total;
  exit;
}
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); exit; }
$eventos = ['visita', 'perfil', 'ficha', 'escrita', 'busca'];
$perfis = ['basico', 'graduacao', 'pos', 'profBasico', 'profSuperior', 'gestorEscolar', 'responsavel'];
$e = $_POST['e'] ?? '';
$p = $_POST['p'] ?? '';
$f = $_POST['f'] ?? '';
if (!in_array($e, $eventos, true)) { http_response_code(400); exit; }
if (!in_array($p, $perfis, true)) $p = '';
if (!preg_match('/^[a-z0-9_]{1,40}$/', $f) || $e !== 'ficha') $f = '';
if ($e === 'ficha' && $f === '') { http_response_code(400); exit; }
$chave = $e . ($p !== '' ? ':' . $p : '') . ($f !== '' ? ':' . $f : '');
date_default_timezone_set('America/Sao_Paulo');
$dia = date('Y-m-d');
$arquivo = __DIR__ . '/contagem/' . date('Y-m') . '.json';
$h = @fopen($arquivo, 'c+');
if (!$h) { http_response_code(500); exit; }
if (flock($h, LOCK_EX)) {
  $dados = json_decode(stream_get_contents($h), true);
  if (!is_array($dados)) $dados = [];
  if (!isset($dados[$dia])) $dados[$dia] = [];
  // Limite de chaves por dia: impede que alguém encha o arquivo com códigos inventados.
  if (isset($dados[$dia][$chave]) || count($dados[$dia]) < 400) {
    $dados[$dia][$chave] = ($dados[$dia][$chave] ?? 0) + 1;
    ftruncate($h, 0);
    rewind($h);
    fwrite($h, json_encode($dados, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
    fflush($h);
  }
  flock($h, LOCK_UN);
}
fclose($h);
http_response_code(204);
