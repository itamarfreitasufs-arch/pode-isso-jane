<?php
// Pode isso, Jane? Painel do contador. Abre só com a chave guardada em contagem/chave.txt:
// painel.php?k=CHAVE
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex, nofollow');
header('Content-Type: text/html; charset=utf-8');
$chave = @trim((string) file_get_contents(__DIR__ . '/contagem/chave.txt'));
if (strlen($chave) < 12 || !hash_equals($chave, (string) ($_GET['k'] ?? ''))) { http_response_code(404); echo 'Não encontrado.'; exit; }
date_default_timezone_set('America/Sao_Paulo');
$dias = [];
foreach (glob(__DIR__ . '/contagem/*.json') ?: [] as $arq) {
  $d = json_decode((string) file_get_contents($arq), true);
  if (is_array($d)) $dias += $d;
}
krsort($dias);
$perguntas = [];
try {
  $db = new PDO('sqlite:' . __DIR__ . '/norma.sqlite', null, null, [PDO::SQLITE_ATTR_OPEN_FLAGS => PDO::SQLITE_OPEN_READONLY]);
  foreach ($db->query('SELECT id, pergunta FROM situacao') as $l) $perguntas[$l['id']] = $l['pergunta'];
} catch (Throwable $t) {}
$nomes = ['basico' => 'Estudante · fundamental e médio', 'graduacao' => 'Estudante · graduação', 'pos' => 'Estudante · pós-graduação', 'profBasico' => 'Professor · fundamental e médio', 'profSuperior' => 'Professor · graduação e pós', 'gestorEscolar' => 'Gestor escolar', 'responsavel' => 'Pai, mãe ou responsável', '' => 'Sem perfil'];
$tot = ['visita' => 0, 'perfil' => 0, 'ficha' => 0, 'escrita' => 0, 'busca' => 0];
$porDia = []; $porPerfil = []; $fichas = [];
foreach ($dias as $dia => $chaves) {
  $linha = ['visita' => 0, 'ficha' => 0, 'escrita' => 0, 'busca' => 0];
  foreach ($chaves as $k => $n) {
    $partes = explode(':', $k);
    $e = $partes[0];
    $p = ($partes[1] ?? '') !== '' && isset($nomes[$partes[1]]) ? $partes[1] : '';
    if (!isset($tot[$e])) continue;
    $tot[$e] += $n;
    if (isset($linha[$e])) $linha[$e] += $n;
    if ($e === 'perfil') $porPerfil[$p]['escolhas'] = ($porPerfil[$p]['escolhas'] ?? 0) + $n;
    if ($e === 'ficha') {
      $porPerfil[$p]['fichas'] = ($porPerfil[$p]['fichas'] ?? 0) + $n;
      $id = end($partes);
      $fichas[$p . ':' . $id] = ($fichas[$p . ':' . $id] ?? 0) + $n;
    }
  }
  $porDia[$dia] = $linha;
}
arsort($fichas);
$h = fn($s) => htmlspecialchars((string) $s, ENT_QUOTES, 'UTF-8');
$num = fn($n) => number_format($n, 0, ',', '.');
?><!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Contador do Jane</title>
<style>
:root{--fundo:#f6f5f1;--texto:#1d1d1b;--suave:#5d5b55;--linha:#dcd9d0;--cartao:#fff}
@media (prefers-color-scheme:dark){:root{--fundo:#1b1b19;--texto:#eceae4;--suave:#a9a69e;--linha:#3a3934;--cartao:#252522}}
body{margin:0;background:var(--fundo);color:var(--texto);font:16px/1.45 system-ui,sans-serif}
main{max-width:760px;margin:0 auto;padding:16px}
h1{font-size:1.4rem;margin:.5rem 0 0}.sub{color:var(--suave);margin:.2rem 0 1rem;font-size:.9rem}
.totais{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px;margin-bottom:1.2rem}
.totais div{background:var(--cartao);border:1px solid var(--linha);border-radius:8px;padding:10px}
.totais b{display:block;font-size:1.5rem;font-variant-numeric:tabular-nums}.totais span{color:var(--suave);font-size:.85rem}
h2{font-size:1.05rem;margin:1.4rem 0 .4rem}
.tabela{overflow-x:auto}table{border-collapse:collapse;width:100%;background:var(--cartao);font-size:.92rem}
th,td{border-bottom:1px solid var(--linha);padding:6px 8px;text-align:left;vertical-align:top}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
p.nota{color:var(--suave);font-size:.85rem}
</style></head><body><main>
<h1>Contador do Pode isso, Jane?</h1>
<p class="sub">Atualizado em <?= $h(date('d/m/Y H:i')) ?> (Brasília). Página só para você: não aparece no app.</p>
<div class="totais">
<div><b><?= $num($tot['visita']) ?></b><span>visitas</span></div>
<div><b><?= $num($tot['ficha']) ?></b><span>fichas abertas</span></div>
<div><b><?= $num($tot['escrita']) ?></b><span>dúvidas escritas</span></div>
<div><b><?= $num($tot['busca']) ?></b><span>buscas na norma</span></div>
</div>
<h2>Por perfil</h2>
<div class="tabela"><table><tr><th>Perfil</th><th class="n">Escolhido</th><th class="n">Fichas abertas</th></tr>
<?php foreach (['basico', 'graduacao', 'pos', 'profBasico', 'profSuperior', 'gestorEscolar', 'responsavel', ''] as $p) if (isset($porPerfil[$p])): ?>
<tr><td><?= $h($nomes[$p]) ?></td><td class="n"><?= $num($porPerfil[$p]['escolhas'] ?? 0) ?></td><td class="n"><?= $num($porPerfil[$p]['fichas'] ?? 0) ?></td></tr>
<?php endif; ?></table></div>
<h2>Fichas mais abertas</h2>
<div class="tabela"><table><tr><th>Ficha</th><th>Perfil</th><th class="n">Vezes</th></tr>
<?php foreach (array_slice($fichas, 0, 30, true) as $k => $n): [$p, $id] = explode(':', $k, 2); ?>
<tr><td><?= $h($perguntas[$id] ?? $id) ?></td><td><?= $h($nomes[$p] ?? '') ?></td><td class="n"><?= $num($n) ?></td></tr>
<?php endforeach; if (!$fichas): ?><tr><td colspan="3">Ainda nenhuma.</td></tr><?php endif; ?></table></div>
<h2>Por dia</h2>
<div class="tabela"><table><tr><th>Dia</th><th class="n">Visitas</th><th class="n">Fichas</th><th class="n">Escritas</th><th class="n">Buscas</th></tr>
<?php foreach (array_slice($porDia, 0, 60, true) as $dia => $l): ?>
<tr><td><?= $h(date('d/m/Y', strtotime($dia))) ?></td><td class="n"><?= $num($l['visita']) ?></td><td class="n"><?= $num($l['ficha']) ?></td><td class="n"><?= $num($l['escrita']) ?></td><td class="n"><?= $num($l['busca']) ?></td></tr>
<?php endforeach; if (!$porDia): ?><tr><td colspan="5">Ainda sem registros.</td></tr><?php endif; ?></table></div>
<p class="nota">Uma visita é uma aba aberta com o app; recarregar não conta de novo. O contador não grava IP, navegador, hora, cookie nem o texto das perguntas: só o dia, o tipo de uso, o perfil e o código da ficha.</p>
</main></body></html>
