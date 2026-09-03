/* ============================================================
   Trabalho Trio - Frontend Prototype
   API Client & Generic CRUD Logic
   ============================================================ */

/**
 * API client for the Trabalho Trio backend (FastAPI).
 * All endpoints return serialized dataclass objects as JSON.
 *
 * API structure:
 *   GET    /<entity>       - list all
 *   POST   /<entity>       - create
 *   GET    /<entity>/{id}  - read one
 *   PUT    /<entity>/{id}  - update
 *   DELETE /<entity>/{id}  - delete
 */

// ---- Base configuration ----
const API_BASE = 'http://127.0.0.1:80';

// ---- Entity field definitions ----
// Each entity defines its fields for table columns and form inputs.
// The `key` maps to the backend field name (as returned by the dataclasses).
const ENTITIES = {
  idiomas: {
    label: 'Idiomas',
    endpoint: 'idiomas',
    idField: 'id',
    fields: [
      { key: 'id', label: 'ID', type: 'number' },
      { key: 'nome', label: 'Nome', type: 'text' },
      { key: 'descricao', label: 'Descrição', type: 'text' }
    ]
  },
  cursos: {
    label: 'Cursos',
    endpoint: 'cursos',
    idField: 'id',
    fields: [
      { key: 'id', label: 'ID', type: 'number' },
      { key: 'id_idioma', label: 'ID Idioma', type: 'number' },
      { key: 'nome', label: 'Nome', type: 'text' },
      { key: 'nivel', label: 'Nível', type: 'number' },
      { key: 'carga_horario', label: 'Carga Horária', type: 'number' },
      { key: 'valor_mensalidade', label: 'Valor Mensalidade', type: 'number' }
    ]
  },
  turmas: {
    label: 'Turmas',
    endpoint: 'turmas',
    idField: 'id_turma',
    fields: [
      { key: 'id_turma', label: 'ID', type: 'number' },
      { key: 'id_professor', label: 'ID Professor', type: 'number' },
      { key: 'id_curso', label: 'ID Curso', type: 'number' },
      { key: 'nome', label: 'Nome', type: 'text' },
      { key: 'horario', label: 'Horário', type: 'text' },
      { key: 'data_inicio', label: 'Data Início', type: 'date' },
      { key: 'data_fim', label: 'Data Fim', type: 'date' },
      { key: 'vagas_totais', label: 'Vagas Totais', type: 'number' }
    ]
  },
  alunos: {
    label: 'Alunos',
    endpoint: 'alunos',
    idField: 'id_aluno',
    fields: [
      { key: 'id_aluno', label: 'ID', type: 'number' },
      { key: 'nome', label: 'Nome', type: 'text' },
      { key: 'cpf', label: 'CPF', type: 'text' },
      { key: 'data_nascimento', label: 'Data Nascimento', type: 'date' },
      { key: 'email', label: 'Email', type: 'email' },
      { key: 'telefone', label: 'Telefone', type: 'text' },
      { key: 'data_cadastro', label: 'Data Cadastro', type: 'date' }
    ]
  },
  escolas: {
    label: 'Escolas',
    endpoint: 'escola',
    idField: 'id_escola',
    fields: [
      { key: 'id_escola', label: 'ID', type: 'number' },
      { key: 'id_curso', label: 'ID Curso', type: 'number' },
      { key: 'nome', label: 'Nome', type: 'text' },
      { key: 'cnpj', label: 'CNPJ', type: 'text' },
      { key: 'endereco', label: 'Endereço', type: 'text' },
      { key: 'telefone', label: 'Telefone', type: 'text' },
      { key: 'email', label: 'Email', type: 'email' }
    ]
  },
  matriculas: {
    label: 'Matrículas',
    endpoint: 'matriculas',
    idField: 'id_matricula',
    fields: [
      { key: 'id_matricula', label: 'ID', type: 'number' },
      { key: 'data_matricula', label: 'Data Matrícula', type: 'date' },
      { key: 'id_aluno', label: 'ID Aluno', type: 'number' },
      { key: 'id_turma', label: 'ID Turma', type: 'number' }
    ]
  },
  professores: {
    label: 'Professores',
    endpoint: 'professores',
    idField: 'id_professor',
    fields: [
      { key: 'id_professor', label: 'ID', type: 'number' },
      { key: 'nome', label: 'Nome', type: 'text' },
      { key: 'cpf', label: 'CPF', type: 'text' },
      { key: 'email', label: 'Email', type: 'email' },
      { key: 'telefone', label: 'Telefone', type: 'text' },
      { key: 'formacao', label: 'Formação', type: 'text' },
      { key: 'data_contratacao', label: 'Data Contratação', type: 'date' }
    ]
  }
};

/**
 * Core API request helper.
 */
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE}/${endpoint}`;
  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options
  });
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API error ${response.status}: ${response.statusText}\n${errorText}`);
  }
  // Some responses (DELETE, PUT returning status only) may not have a body
  const text = await response.text();
  return text ? JSON.parse(text) : null;
}

/**
 * CRUD operations for a given entity.
 */
const api = {
  list(endpoint) {
    return apiRequest(endpoint);
  },
  get(endpoint, id) {
    return apiRequest(`${endpoint}/${id}`);
  },
  create(endpoint, data) {
    return apiRequest(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  },
  update(endpoint, id, data) {
    return apiRequest(`${endpoint}/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  },
  delete(endpoint, id) {
    return apiRequest(`${endpoint}/${id}`, {
      method: 'DELETE'
    });
  }
};

/**
 * Render breadcrumbs for the current page.
 * @param {Array} crumbs - Array of { label, href } objects.
 * The last item is rendered as the current page (not a link).
 */
function renderBreadcrumbs(crumbs) {
  const container = document.getElementById('breadcrumbs');
  if (!container) return;

  const html = crumbs.map((crumb, index) => {
    if (index === crumbs.length - 1) {
      return `<span class="current">${crumb.label}</span>`;
    }
    return `<a href="${crumb.href}">${crumb.label}</a>`;
  }).join('<span class="separator">›</span>');

  container.innerHTML = html;
}

/**
 * Show an alert message.
 */
function showAlert(message, type = 'success') {
  const alertEl = document.getElementById('alert');
  if (!alertEl) return;

  alertEl.textContent = message;
  alertEl.className = `alert alert-${type} show`;

  setTimeout(() => {
    alertEl.classList.remove('show');
  }, 4000);
}

/**
 * Format a value for table display.
 */
function formatValue(value, type) {
  if (value === null || value === undefined || value === '') {
    return '-';
  }
  if (type === 'date' && value) {
    const d = new Date(value);
    if (!isNaN(d.getTime())) {
      return d.toLocaleDateString('pt-BR');
    }
  }
  if (type === 'number' && typeof value === 'number' && value % 1 !== 0) {
    return value.toFixed(2);
  }
  return value;
}
