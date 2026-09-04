// ============================================================
// Escola de Idiomas — frontend estático (sem build step).
// Conecta diretamente na API FastAPI via fetch().
// ============================================================

const DEFAULT_API_BASE = "http://127.0.0.1:8000";

// ---------- configuração de cada entidade ----------
// `columns`  -> como cada campo aparece na tabela de listagem
// `fields`   -> como cada campo aparece no formulário de criar/editar
// `optionLabel` -> como o registro aparece dentro de um <select> de outra entidade

const ENTITIES = {
  idiomas: {
    label: "Idiomas",
    singular: "idioma",
    gender: "m",
    endpoint: "/idiomas",
    pk: "id",
    description: "Idiomas oferecidos pela escola.",
    optionLabel: (r) => r.nome,
    columns: [
      { key: "id", label: "ID", type: "id" },
      { key: "nome", label: "Nome" },
      { key: "descricao", label: "Descrição" },
    ],
    fields: [
      { name: "nome", label: "Nome do idioma", type: "text", required: true, placeholder: "Inglês" },
      { name: "descricao", label: "Descrição", type: "textarea", required: false, placeholder: "Breve descrição do idioma e do programa" },
    ],
  },

  cursos: {
    label: "Cursos",
    singular: "curso",
    gender: "m",
    endpoint: "/cursos",
    pk: "id",
    description: "Cursos vinculados a um idioma, com nível e carga horária.",
    optionLabel: (r) => `${r.nome} (nível ${r.nivel})`,
    columns: [
      { key: "id", label: "ID", type: "id" },
      { key: "id_idioma", label: "Idioma", type: "lookup", ref: "idiomas" },
      { key: "nome", label: "Nome" },
      { key: "nivel", label: "Nível", type: "num" },
      { key: "carga_horario", label: "Carga horária", type: "num", suffix: "h" },
      { key: "valor_mensalidade", label: "Mensalidade", type: "currency" },
    ],
    fields: [
      { name: "id_idioma", label: "Idioma", type: "select", ref: "idiomas", required: true },
      { name: "nome", label: "Nome do curso", type: "text", required: true, placeholder: "Inglês Básico" },
      { name: "nivel", label: "Nível", type: "number", required: true, placeholder: "1" },
      { name: "carga_horario", label: "Carga horária (horas)", type: "number", required: true, placeholder: "60" },
      { name: "valor_mensalidade", label: "Mensalidade (R$)", type: "number", step: "0.01", required: true, placeholder: "250.00" },
    ],
  },

  professores: {
    label: "Professores",
    singular: "professor",
    gender: "m",
    endpoint: "/professores",
    pk: "id_professor",
    description: "Corpo docente responsável pelas turmas.",
    optionLabel: (r) => r.nome,
    columns: [
      { key: "id_professor", label: "ID", type: "id" },
      { key: "nome", label: "Nome" },
      { key: "cpf", label: "CPF" },
      { key: "email", label: "Email" },
      { key: "telefone", label: "Telefone" },
      { key: "formacao", label: "Formação" },
      { key: "data_contratacao", label: "Contratação", type: "date" },
    ],
    fields: [
      { name: "nome", label: "Nome completo", type: "text", required: true },
      { name: "cpf", label: "CPF (somente números)", type: "text", required: true, maxlength: 11, placeholder: "00000000000" },
      { name: "email", label: "Email", type: "email", required: false },
      { name: "telefone", label: "Telefone", type: "text", required: false, placeholder: "(47) 90000-0000" },
      { name: "formacao", label: "Formação", type: "text", required: false, placeholder: "Letras - Inglês" },
      { name: "data_contratacao", label: "Data de contratação", type: "date", required: true, defaultToday: true },
    ],
  },

  turmas: {
    label: "Turmas",
    singular: "turma",
    gender: "f",
    endpoint: "/turmas",
    pk: "id_turma",
    description: "Turmas abertas, cada uma vinculada a um curso e a um professor.",
    optionLabel: (r) => r.nome,
    columns: [
      { key: "id_turma", label: "ID", type: "id" },
      { key: "id_curso", label: "Curso", type: "lookup", ref: "cursos" },
      { key: "id_professor", label: "Professor", type: "lookup", ref: "professores" },
      { key: "nome", label: "Turma" },
      { key: "horario", label: "Horário" },
      { key: "data_inicio", label: "Início", type: "date" },
      { key: "data_fim", label: "Fim", type: "date" },
      { key: "vagas_totais", label: "Vagas", type: "num" },
    ],
    fields: [
      { name: "id_curso", label: "Curso", type: "select", ref: "cursos", required: true },
      { name: "id_professor", label: "Professor", type: "select", ref: "professores", required: true },
      { name: "nome", label: "Nome da turma", type: "text", required: true, placeholder: "Turma A" },
      { name: "horario", label: "Horário", type: "text", required: true, placeholder: "Seg e Qua, 19h às 21h" },
      { name: "data_inicio", label: "Data de início", type: "date", required: true },
      { name: "data_fim", label: "Data de encerramento", type: "date", required: true },
      { name: "vagas_totais", label: "Vagas totais", type: "number", required: true, placeholder: "20" },
    ],
  },

  alunos: {
    label: "Alunos",
    singular: "aluno",
    gender: "m",
    endpoint: "/alunos",
    pk: "id_aluno",
    description: "Alunos cadastrados na secretaria.",
    optionLabel: (r) => r.nome,
    columns: [
      { key: "id_aluno", label: "ID", type: "id" },
      { key: "nome", label: "Nome" },
      { key: "cpf", label: "CPF" },
      { key: "email", label: "Email" },
      { key: "telefone", label: "Telefone" },
      { key: "data_nascimento", label: "Nascimento", type: "date" },
      { key: "data_cadastro", label: "Cadastro", type: "date" },
    ],
    fields: [
      { name: "nome", label: "Nome completo", type: "text", required: true },
      { name: "cpf", label: "CPF (somente números)", type: "text", required: true, maxlength: 11, placeholder: "00000000000" },
      { name: "data_nascimento", label: "Data de nascimento", type: "date", required: true },
      { name: "email", label: "Email", type: "email", required: false },
      { name: "telefone", label: "Telefone", type: "text", required: false, placeholder: "(47) 90000-0000" },
      { name: "data_cadastro", label: "Data de cadastro", type: "date", required: true, defaultToday: true },
    ],
  },

  matriculas: {
    label: "Matrículas",
    singular: "matrícula",
    gender: "f",
    endpoint: "/matriculas",
    pk: "id_matricula",
    description: "Vínculo entre um aluno e uma turma.",
    optionLabel: (r) => `#${r.id_matricula}`,
    columns: [
      { key: "id_matricula", label: "ID", type: "id" },
      { key: "id_aluno", label: "Aluno", type: "lookup", ref: "alunos" },
      { key: "id_turma", label: "Turma", type: "lookup", ref: "turmas" },
      { key: "data_matricula", label: "Data", type: "date" },
    ],
    fields: [
      { name: "id_aluno", label: "Aluno", type: "select", ref: "alunos", required: true },
      { name: "id_turma", label: "Turma", type: "select", ref: "turmas", required: true },
      { name: "data_matricula", label: "Data da matrícula", type: "date", required: true, defaultToday: true },
    ],
  },

  escola: {
    label: "Escola",
    singular: "unidade",
    gender: "f",
    endpoint: "/escola",
    pk: "id_escola",
    description: "Unidades da escola, cada uma vinculada a um curso.",
    optionLabel: (r) => r.nome,
    columns: [
      { key: "id_escola", label: "ID", type: "id" },
      { key: "id_curso", label: "Curso vinculado", type: "lookup", ref: "cursos" },
      { key: "nome", label: "Nome" },
      { key: "cnpj", label: "CNPJ" },
      { key: "endereco", label: "Endereço" },
      { key: "telefone", label: "Telefone" },
      { key: "email", label: "Email" },
    ],
    fields: [
      { name: "id_curso", label: "Curso vinculado", type: "select", ref: "cursos", required: true },
      { name: "nome", label: "Nome da unidade", type: "text", required: true },
      { name: "cnpj", label: "CNPJ (somente números)", type: "text", required: true, maxlength: 14 },
      { name: "endereco", label: "Endereço", type: "text", required: false },
      { name: "telefone", label: "Telefone", type: "text", required: false },
      { name: "email", label: "Email", type: "email", required: false },
    ],
  },
};

const ENTITY_ORDER = ["idiomas", "cursos", "professores", "turmas", "alunos", "matriculas", "escola"];

// ---------- estado ----------

const state = {
  apiBase: localStorage.getItem("escola_api_base") || DEFAULT_API_BASE,
  currentKey: ENTITY_ORDER[0],
  records: [],
};

// ---------- elementos ----------

const el = {
  navList: document.getElementById("nav-list"),
  apiBaseInput: document.getElementById("api-base"),
  connStatus: document.getElementById("conn-status"),
  title: document.getElementById("section-title"),
  sub: document.getElementById("section-sub"),
  btnNew: document.getElementById("btn-new"),
  errorBanner: document.getElementById("error-banner"),
  errorText: document.getElementById("error-text"),
  btnRetry: document.getElementById("btn-retry"),
  tableWrap: document.getElementById("table-wrap"),
  tableHead: document.getElementById("table-head"),
  tableBody: document.getElementById("table-body"),
  emptyState: document.getElementById("empty-state"),
  emptyText: document.getElementById("empty-text"),
  btnEmptyNew: document.getElementById("btn-empty-new"),
  loadingState: document.getElementById("loading-state"),
  overlay: document.getElementById("overlay"),
  panel: document.getElementById("panel"),
  panelForm: document.getElementById("panel-form"),
  panelTitle: document.getElementById("panel-title"),
  panelFields: document.getElementById("panel-fields"),
  panelError: document.getElementById("panel-error"),
  btnClose: document.getElementById("btn-close"),
  btnCancel: document.getElementById("btn-cancel"),
  toast: document.getElementById("toast"),
};

// ---------- api helper ----------

async function apiFetch(path, options = {}) {
  const base = state.apiBase.replace(/\/+$/, "");
  const url = base + path;
  let res;
  try {
    res = await fetch(url, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch (err) {
    throw new Error(
      `Não foi possível conectar em ${base}. Confira se o backend está rodando (uvicorn) e se o endereço da API, no rodapé do menu, está correto.`
    );
  }

  if (!res.ok) {
    let detail = "";
    try {
      const body = await res.json();
      detail = body.detail || JSON.stringify(body);
    } catch (e) {
      /* corpo vazio ou não é JSON */
    }
    throw new Error(detail || `A API respondeu com erro ${res.status}.`);
  }

  const text = await res.text();
  return text ? JSON.parse(text) : null;
}

const listCache = {};

async function fetchList(key, { fresh = false } = {}) {
  if (!fresh && listCache[key]) return listCache[key];
  const data = await apiFetch(ENTITIES[key].endpoint);
  listCache[key] = data || [];
  return listCache[key];
}

// ---------- formatação ----------

function formatDateBR(iso) {
  if (!iso) return "—";
  const datePart = String(iso).split("T")[0];
  const parts = datePart.split("-");
  if (parts.length !== 3) return datePart;
  const [y, m, d] = parts;
  return `${d}/${m}/${y}`;
}

function formatCurrency(value) {
  const n = Number(value);
  if (Number.isNaN(n)) return "—";
  return n.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function todayISO() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

// ---------- navegação ----------

function renderNav() {
  el.navList.innerHTML = "";
  ENTITY_ORDER.forEach((key) => {
    const entity = ENTITIES[key];
    const li = document.createElement("li");
    const btn = document.createElement("button");
    btn.className = "nav-item" + (key === state.currentKey ? " active" : "");
    btn.textContent = entity.label;
    btn.addEventListener("click", () => selectEntity(key));
    li.appendChild(btn);
    el.navList.appendChild(li);
  });
}

function selectEntity(key) {
  state.currentKey = key;
  renderNav();
  loadSection(key);
}

// ---------- carregar e renderizar seção ----------

async function loadSection(key) {
  const entity = ENTITIES[key];
  el.title.textContent = entity.label;
  el.sub.textContent = entity.description;

  el.errorBanner.hidden = true;
  el.emptyState.hidden = true;
  el.tableWrap.querySelector("table").style.display = "none";
  el.loadingState.hidden = false;

  try {
    const refKeys = [...new Set(entity.columns.filter((c) => c.type === "lookup").map((c) => c.ref))];
    const [records] = await Promise.all([fetchList(key, { fresh: true }), ...refKeys.map((r) => fetchList(r))]);

    state.records = records;
    renderTable(entity, records, refKeys);
  } catch (err) {
    el.loadingState.hidden = true;
    el.errorBanner.hidden = false;
    el.errorText.textContent = err.message;
  }
}

function renderTable(entity, records, refKeys) {
  el.loadingState.hidden = true;

  const lookups = {};
  refKeys.forEach((r) => {
    lookups[r] = new Map((listCache[r] || []).map((rec) => [rec[ENTITIES[r].pk], rec]));
  });

  el.tableHead.innerHTML = "";
  const headRow = document.createElement("tr");
  entity.columns.forEach((col) => {
    const th = document.createElement("th");
    th.textContent = col.label;
    headRow.appendChild(th);
  });
  headRow.appendChild(document.createElement("th"));
  el.tableHead.appendChild(headRow);

  el.tableBody.innerHTML = "";

  if (!records || records.length === 0) {
    el.tableWrap.querySelector("table").style.display = "none";
    el.emptyState.hidden = false;
    el.emptyText.textContent = noneLabel(entity);
    return;
  }

  el.emptyState.hidden = true;
  el.tableWrap.querySelector("table").style.display = "table";

  records.forEach((record) => {
    const tr = document.createElement("tr");

    entity.columns.forEach((col) => {
      const td = document.createElement("td");
      const raw = record[col.key];

      if (col.type === "id") {
        td.className = "id-col";
        td.textContent = raw;
      } else if (col.type === "num") {
        td.className = "num";
        td.textContent = raw === null || raw === undefined ? "—" : `${raw}${col.suffix || ""}`;
      } else if (col.type === "currency") {
        td.className = "num";
        td.textContent = formatCurrency(raw);
      } else if (col.type === "date") {
        td.className = "num";
        td.textContent = formatDateBR(raw);
      } else if (col.type === "lookup") {
        const refRecord = lookups[col.ref] && lookups[col.ref].get(raw);
        td.textContent = refRecord ? ENTITIES[col.ref].optionLabel(refRecord) : `#${raw}`;
      } else {
        td.textContent = raw === null || raw === undefined || raw === "" ? "—" : raw;
      }

      tr.appendChild(td);
    });

    const tdActions = document.createElement("td");
    tdActions.className = "actions";

    const btnEdit = document.createElement("button");
    btnEdit.type = "button";
    btnEdit.className = "btn-text edit";
    btnEdit.textContent = "Editar";
    btnEdit.addEventListener("click", () => openPanel("edit", entity, record));

    const btnDel = document.createElement("button");
    btnDel.type = "button";
    btnDel.className = "btn-text danger";
    btnDel.textContent = "Excluir";
    btnDel.addEventListener("click", () => confirmDelete(entity, record));

    tdActions.appendChild(btnEdit);
    tdActions.appendChild(btnDel);
    tr.appendChild(tdActions);

    el.tableBody.appendChild(tr);
  });
}

// ---------- painel de criar/editar ----------

let currentEntityForPanel = null;
let currentRecordForPanel = null;

async function openPanel(mode, entity, record = null) {
  currentEntityForPanel = entity;
  currentRecordForPanel = record;

  el.panelTitle.textContent = mode === "edit" ? `Editar ${entity.singular}` : newLabel(entity);
  el.panelError.hidden = true;
  el.panelFields.innerHTML = "<p class='hint'>Carregando formulário…</p>";

  showPanel();

  try {
    const fieldEls = await Promise.all(entity.fields.map((f) => buildField(f, record)));
    el.panelFields.innerHTML = "";
    fieldEls.forEach((node) => el.panelFields.appendChild(node));
  } catch (err) {
    el.panelFields.innerHTML = "";
    el.panelError.hidden = false;
    el.panelError.textContent = err.message;
  }
}

async function buildField(field, record) {
  const wrap = document.createElement("div");
  wrap.className = "field";

  const label = document.createElement("label");
  label.textContent = field.label + (field.required ? "" : " (opcional)");
  label.setAttribute("for", "f_" + field.name);
  wrap.appendChild(label);

  let input;

  if (field.type === "textarea") {
    input = document.createElement("textarea");
  } else if (field.type === "select") {
    input = document.createElement("select");
    const blank = document.createElement("option");
    blank.value = "";
    blank.textContent = "Selecione…";
    input.appendChild(blank);

    const options = await fetchList(field.ref);
    options.forEach((opt) => {
      const optionEl = document.createElement("option");
      const pk = ENTITIES[field.ref].pk;
      optionEl.value = opt[pk];
      optionEl.textContent = ENTITIES[field.ref].optionLabel(opt);
      input.appendChild(optionEl);
    });
  } else {
    input = document.createElement("input");
    input.type = field.type === "number" ? "number" : field.type === "date" ? "date" : field.type === "email" ? "email" : "text";
    if (field.step) input.step = field.step;
    if (field.maxlength) input.maxLength = field.maxlength;
    if (field.placeholder) input.placeholder = field.placeholder;
  }

  input.id = "f_" + field.name;
  input.name = field.name;
  if (field.required) input.required = true;

  if (record && record[field.name] !== undefined && record[field.name] !== null) {
    input.value = String(record[field.name]).split("T")[0];
  } else if (field.defaultToday) {
    input.value = todayISO();
  }

  wrap.appendChild(input);
  return wrap;
}

function showPanel() {
  el.overlay.hidden = false;
  el.panel.hidden = false;
}

function closePanel() {
  el.overlay.hidden = true;
  el.panel.hidden = true;
  currentEntityForPanel = null;
  currentRecordForPanel = null;
}

el.panelForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!currentEntityForPanel) return;

  const entity = currentEntityForPanel;
  const formData = new FormData(el.panelForm);
  const payload = {};

  entity.fields.forEach((f) => {
    let value = formData.get(f.name);
    if (f.type === "number") {
      value = value === "" ? null : Number(value);
    } else if (value === "") {
      value = null;
    }
    payload[f.name] = value;
  });

  el.panelError.hidden = true;

  try {
    if (currentRecordForPanel) {
      await apiFetch(`${entity.endpoint}/${currentRecordForPanel[entity.pk]}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });
      showToast(actionMessage(entity, "update"));
    } else {
      await apiFetch(entity.endpoint, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      showToast(actionMessage(entity, "create"));
    }

    // qualquer entidade pode aparecer como lookup em outra tela — mais simples invalidar tudo
    Object.keys(listCache).forEach((k) => delete listCache[k]);

    closePanel();
    loadSection(state.currentKey);
  } catch (err) {
    el.panelError.hidden = false;
    el.panelError.textContent = err.message;
  }
});

function capitalize(s) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

const PARTICIPLES = {
  create: { m: "cadastrado", f: "cadastrada" },
  update: { m: "atualizado", f: "atualizada" },
  delete: { m: "excluído", f: "excluída" },
};

function newLabel(entity) {
  return `${entity.gender === "f" ? "Nova" : "Novo"} ${entity.singular}`;
}

function noneLabel(entity) {
  const artigo = entity.gender === "f" ? "Nenhuma" : "Nenhum";
  return `${artigo} ${entity.singular} cadastrad${entity.gender === "f" ? "a" : "o"} ainda.`;
}

function actionMessage(entity, action) {
  return `${capitalize(entity.singular)} ${PARTICIPLES[action][entity.gender]}.`;
}

// ---------- excluir ----------

async function confirmDelete(entity, record) {
  const label = entity.optionLabel(record) || `#${record[entity.pk]}`;
  const ok = window.confirm(`Excluir ${entity.singular} "${label}"? Essa ação não pode ser desfeita.`);
  if (!ok) return;

  try {
    await apiFetch(`${entity.endpoint}/${record[entity.pk]}`, { method: "DELETE" });
    Object.keys(listCache).forEach((k) => delete listCache[k]);
    showToast(actionMessage(entity, "delete"));
    loadSection(state.currentKey);
  } catch (err) {
    showToast(err.message, true);
  }
}

// ---------- toast ----------

let toastTimer = null;

function showToast(message, danger = false) {
  el.toast.textContent = message;
  el.toast.className = "toast" + (danger ? " danger" : "");
  el.toast.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    el.toast.hidden = true;
  }, 3000);
}

// ---------- endereço da API ----------

function updateConnStatusIdle() {
  el.connStatus.textContent = "";
  el.connStatus.className = "conn-status";
}

el.apiBaseInput.addEventListener("change", () => {
  const value = el.apiBaseInput.value.trim() || DEFAULT_API_BASE;
  state.apiBase = value;
  localStorage.setItem("escola_api_base", value);
  Object.keys(listCache).forEach((k) => delete listCache[k]);
  updateConnStatusIdle();
  loadSection(state.currentKey);
});

// ---------- eventos gerais ----------

el.btnNew.addEventListener("click", () => openPanel("create", ENTITIES[state.currentKey]));
el.btnEmptyNew.addEventListener("click", () => openPanel("create", ENTITIES[state.currentKey]));
el.btnClose.addEventListener("click", closePanel);
el.btnCancel.addEventListener("click", closePanel);
el.overlay.addEventListener("click", closePanel);
el.btnRetry.addEventListener("click", () => loadSection(state.currentKey));

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && !el.panel.hidden) closePanel();
});

// ---------- inicialização ----------

el.apiBaseInput.value = state.apiBase;
renderNav();
loadSection(state.currentKey);
