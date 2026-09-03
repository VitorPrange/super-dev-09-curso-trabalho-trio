/* ============================================================
   Trabalho Trio - Frontend Prototype
   Generic CRUD Application Logic
   ============================================================ */

/**
 * Generic CRUD application that works for all entities.
 * Initializes on DOMContentLoaded and reads the entity key
 * from a data attribute on the page root element.
 */

document.addEventListener('DOMContentLoaded', function () {
  const root = document.getElementById('crud-root');
  if (!root) return; // Not a CRUD page

  const entityKey = root.dataset.entity;
  const config = ENTITIES[entityKey];
  if (!config) return;

  const tableBody = document.getElementById('table-body');
  const form = document.getElementById('crud-form');
  const formTitle = document.getElementById('form-title');
  let editingId = null;

  // ---- Render form fields dynamically ----
  function renderForm() {
    // Use all fields except the ID field for the form
    const formFields = config.fields.filter(f => f.key !== config.idField);

    form.innerHTML = '';

    // Render fields in two-column grid
    let row = document.createElement('div');
    row.className = 'form-row';

    formFields.forEach(field => {
      const group = document.createElement('div');
      group.className = 'form-group';

      const label = document.createElement('label');
      label.textContent = field.label;
      label.htmlFor = field.key;

      const input = document.createElement(field.type === 'textarea' ? 'textarea' : 'input');
      input.type = field.type;
      input.id = field.key;
      input.name = field.key;
      input.required = true;

      group.appendChild(label);
      group.appendChild(input);

      // Add to current row or create new row
      if (row.children.length >= 2) {
        form.appendChild(row);
        row = document.createElement('div');
        row.className = 'form-row';
      }
      row.appendChild(group);
    });

    if (row.children.length > 0) {
      form.appendChild(row);
    }

    // Form actions
    const actions = document.createElement('div');
    actions.className = 'form-actions';

    const cancel = document.createElement('button');
    cancel.type = 'button';
    cancel.className = 'btn btn-secondary';
    cancel.id = 'btn-cancel';
    cancel.textContent = 'Cancelar';

    const submit = document.createElement('button');
    submit.type = 'submit';
    submit.className = 'btn';
    submit.textContent = 'Salvar';

    actions.appendChild(cancel);
    actions.appendChild(submit);
    form.appendChild(actions);
  }

  // ---- Render table ----
  async function renderTable() {
    tableBody.innerHTML = '<tr><td colspan="100%"><div class="loading"><div class="spinner"></div><p>Carregando...</p></div></td></tr>';

    try {
      const data = await api.list(config.endpoint);
      tableBody.innerHTML = '';

      if (!data || data.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="100%"><div class="empty-state"><div class="icon">📋</div><p>Nenhum registro encontrado.</p></div></td></tr>';
        return;
      }

      data.forEach(item => {
        const tr = document.createElement('tr');

        // ID column
        const idTd = document.createElement('td');
        idTd.textContent = item[config.idField];
        idTd.className = 'id-cell';

        // Data columns (exclude ID field)
        const dataFields = config.fields.filter(f => f.key !== config.idField);
        const dataTds = dataFields.map(field => {
          const td = document.createElement('td');
          td.textContent = formatValue(item[field.key], field.type);
          return td;
        });

        // Action column
        const actionTd = document.createElement('td');
        actionTd.className = 'action-cell';
        actionTd.innerHTML = `
          <div class="action-buttons">
            <button class="action-btn edit" onclick="app.editItem('${item[config.idField]}')">✏️</button>
            <button class="action-btn delete" onclick="app.deleteItem('${item[config.idField]}')">🗑</button>
          </div>
        `;

        tr.appendChild(idTd);
        dataTds.forEach(td => tr.appendChild(td));
        tr.appendChild(actionTd);
        tableBody.appendChild(tr);
      });
    } catch (error) {
      tableBody.innerHTML = '<tr><td colspan="100%"><div class="empty-state"><div class="icon">⚠️</div><p>Erro ao carregar dados. Verifique se o backend está rodando.</p></div></td></tr>';
      console.error('Failed to load', config.label, error);
    }
  }

  // ---- Render table headers ----
  function renderTableHeaders() {
    const thead = document.querySelector('thead');
    if (!thead) return;

    const dataFields = config.fields.filter(f => f.key !== config.idField);
    let html = '<tr>';
    html += `<th>ID</th>`;
    dataFields.forEach(f => {
      html += `<th>${f.label}</th>`;
    });
    html += `<th>Ações</th>`;
    html += '</tr>';
    thead.innerHTML = html;
  }

  // ---- Form submission ----
  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    const formData = new FormData(form);
    const data = {};

    formData.forEach((value, key) => {
      const field = config.fields.find(f => f.key === key);
      if (field && field.type === 'number') {
        data[key] = parseFloat(value) || 0;
      } else if (field && field.type === 'date') {
        data[key] = value;
      } else {
        data[key] = value;
      }
    });

    try {
      if (editingId !== null) {
        await api.update(config.endpoint, editingId, data);
        showAlert(`${config.label} atualizado com sucesso!`, 'success');
        editingId = null;
        formTitle.textContent = `Novo ${config.label.slice(0, -1)}`;
      } else {
        await api.create(config.endpoint, data);
        showAlert(`${config.label} cadastrado com sucesso!`, 'success');
      }

      form.reset();
      await renderTable();
    } catch (error) {
      showAlert(`Erro ao salvar: ${error.message}`, 'error');
      console.error('Save error:', error);
    }
  });

  // ---- Cancel edit ----
  function attachCancelHandler() {
    const cancelBtn = document.getElementById('btn-cancel');
    if (cancelBtn) {
      cancelBtn.addEventListener('click', function () {
        editingId = null;
        form.reset();
        formTitle.textContent = `Novo ${config.label.slice(0, -1)}`;
      });
    }
  }

  // ---- Edit item ----
  async function editItem(id) {
    try {
      const item = await api.get(config.endpoint, id);
      const formFields = config.fields.filter(f => f.key !== config.idField);

      formFields.forEach(field => {
        const input = form.querySelector(`[name="${field.key}"]`);
        if (input) {
          input.value = item[field.key] || '';
        }
      });

      editingId = id;
      formTitle.textContent = `Editar ${config.label.slice(0, -1)}`;
    } catch (error) {
      showAlert(`Erro ao carregar item: ${error.message}`, 'error');
      console.error('Edit error:', error);
    }
  }

  // ---- Delete item ----
  async function deleteItem(id) {
    const overlay = document.getElementById('modal-overlay');
    const confirmBtn = document.getElementById('modal-confirm');

    overlay.classList.add('active');

    const cleanup = () => {
      overlay.classList.remove('active');
      confirmBtn.removeEventListener('click', onConfirm);
      cancelModal.removeEventListener('click', onCancel);
    };

    const onConfirm = async () => {
      cleanup();
      try {
        await api.delete(config.endpoint, id);
        showAlert(`${config.label} removido com sucesso!`, 'success');
        await renderTable();
      } catch (error) {
        showAlert(`Erro ao remover: ${error.message}`, 'error');
        console.error('Delete error:', error);
      }
    };

    const onCancel = () => {
      cleanup();
    };

    const cancelModal = document.getElementById('modal-cancel');
    confirmBtn.addEventListener('click', onConfirm);
    cancelModal.addEventListener('click', onCancel);
  }

  // ---- Public API for inline onclick ----
  window.app = {
    editItem,
    deleteItem
  };

  // ---- Initialize ----
  renderForm();
  attachCancelHandler();
  renderTableHeaders();
  renderTable();
});
