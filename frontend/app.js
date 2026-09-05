const api = '/api';

const $ = (selector) => document.querySelector(selector);

function showToast(message) {
    const toast = $('#toast');
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2500);
}

async function request(path, options = {}) {
    const response = await fetch(`${api}${path}`, {
        headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
        ...options,
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Request failed');
    return data;
}

function formDataToObject(form) {
    const data = Object.fromEntries(new FormData(form).entries());
    for (const key of Object.keys(data)) {
        if (data[key] === '') data[key] = null;
    }
    return data;
}

async function loadDashboard() {
    const data = await request('/dashboard');
    $('#studentsCount').textContent = data.students;
    $('#companiesCount').textContent = data.companies;
    $('#jobsCount').textContent = data.jobs;
    $('#applicationsCount').textContent = data.applications;
    $('#selectedCount').textContent = data.selected;
}

async function loadJobs() {
    const search = encodeURIComponent($('#jobSearch').value.trim());
    const location = encodeURIComponent($('#jobLocation').value.trim());
    const query = [`search=${search}`, `location=${location}`].filter(Boolean).join('&');
    const jobs = await request(`/jobs?${query}`);
    const container = $('#jobsList');

    if (!jobs.length) {
        container.innerHTML = '<p>No jobs found.</p>';
        return;
    }

    container.innerHTML = jobs.map(job => `
        <article class="job-card">
            <h3>${escapeHtml(job.title)}</h3>
            <div class="company">${escapeHtml(job.company)}</div>
            <div class="meta">${escapeHtml(job.location)} · ${escapeHtml(job.salary || 'Salary not specified')}</div>
            <div class="meta">Internship: ${escapeHtml(job.internship_duration || 'N/A')} · Stipend: ${escapeHtml(job.stipend || 'N/A')}</div>
            <p>${escapeHtml(job.description || '')}</p>
            <div class="skills"><strong>Skills:</strong> ${escapeHtml(job.skills || 'Not specified')}</div>
            <button class="apply-btn" data-job-id="${job.id}">Apply</button>
        </article>
    `).join('');

    container.querySelectorAll('.apply-btn').forEach(button => {
        button.addEventListener('click', () => applyForJob(Number(button.dataset.jobId)));
    });
}

async function applyForJob(jobId) {
    const students = await request('/students');
    if (!students.length) {
        showToast('Create a student profile first.');
        document.querySelector('[data-section="studentSection"]').click();
        return;
    }
    const studentId = Number(prompt(`Enter Student ID to apply (available IDs: ${students.map(s => s.id).join(', ')})`));
    if (!studentId) return;

    try {
        await request('/applications', {
            method: 'POST',
            body: JSON.stringify({ student_id: studentId, job_id: jobId })
        });
        showToast('Application submitted successfully.');
        await Promise.all([loadDashboard(), loadApplications()]);
    } catch (error) {
        showToast(error.message);
    }
}

async function loadStudents() {
    const students = await request('/students');
    $('#studentsList').innerHTML = students.length ? `
        <table>
            <thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Course</th><th>Year</th><th>Percentage</th></tr></thead>
            <tbody>${students.map(s => `
                <tr><td>${s.id}</td><td>${escapeHtml(s.name)}</td><td>${escapeHtml(s.email)}</td>
                <td>${escapeHtml(s.course)}</td><td>${s.graduation_year ?? ''}</td><td>${s.percentage ?? ''}</td></tr>
            `).join('')}</tbody>
        </table>` : '<p>No students yet.</p>';
}

async function loadApplications() {
    const applications = await request('/applications');
    $('#applicationsList').innerHTML = applications.length ? `
        <table>
            <thead><tr><th>ID</th><th>Student</th><th>Company</th><th>Job</th><th>Location</th><th>Status</th><th>Applied</th></tr></thead>
            <tbody>${applications.map(a => `
                <tr>
                    <td>${a.id}</td><td>${escapeHtml(a.student)}</td><td>${escapeHtml(a.company)}</td>
                    <td>${escapeHtml(a.job)}</td><td>${escapeHtml(a.location)}</td>
                    <td><select class="status-select" data-application-id="${a.id}">
                        ${['Applied','Shortlisted','Interview','Selected','Rejected'].map(status => `<option ${status === a.status ? 'selected' : ''}>${status}</option>`).join('')}
                    </select></td>
                    <td>${formatDate(a.applied_at)}</td>
                </tr>
            `).join('')}</tbody>
        </table>` : '<p>No applications yet.</p>';

    document.querySelectorAll('.status-select').forEach(select => {
        select.addEventListener('change', async () => {
            try {
                await request(`/applications/${select.dataset.applicationId}/status`, {
                    method: 'PATCH', body: JSON.stringify({ status: select.value })
                });
                showToast('Application status updated.');
                await loadDashboard();
            } catch (error) { showToast(error.message); }
        });
    });
}

async function loadInterviews() {
    const interviews = await request('/interviews');
    $('#interviewsList').innerHTML = interviews.length ? `
        <table>
            <thead><tr><th>ID</th><th>Student</th><th>Company</th><th>Job</th><th>Round</th><th>Scheduled</th><th>Mode</th><th>Notes</th></tr></thead>
            <tbody>${interviews.map(i => `
                <tr><td>${i.id}</td><td>${escapeHtml(i.student)}</td><td>${escapeHtml(i.company)}</td>
                <td>${escapeHtml(i.job)}</td><td>${escapeHtml(i.round_name)}</td><td>${formatDate(i.scheduled_at)}</td>
                <td>${escapeHtml(i.mode)}</td><td>${escapeHtml(i.notes || '')}</td></tr>
            `).join('')}</tbody>
        </table>` : '<p>No interviews scheduled yet.</p>';
}

async function loadCompanies() {
    const companies = await request('/companies');
    $('#companiesList').innerHTML = companies.length ? `
        <table>
            <thead><tr><th>ID</th><th>Name</th><th>Location</th><th>Website</th><th>Description</th></tr></thead>
            <tbody>${companies.map(c => `
                <tr><td>${c.id}</td><td>${escapeHtml(c.name)}</td><td>${escapeHtml(c.location)}</td>
                <td>${c.website ? `<a href="${c.website}" target="_blank">Open</a>` : ''}</td>
                <td>${escapeHtml(c.description || '')}</td></tr>
            `).join('')}</tbody>
        </table>` : '<p>No companies yet.</p>';
}

function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>'"]/g, char => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
    })[char]);
}

function formatDate(value) {
    if (!value) return '';
    return new Date(value).toLocaleString();
}

async function createStudent(event) {
    event.preventDefault();
    try {
        const data = formDataToObject(event.target);
        for (const key of ['graduation_year']) if (data[key]) data[key] = Number(data[key]);
        if (data.percentage) data.percentage = Number(data.percentage);
        await request('/students', { method: 'POST', body: JSON.stringify(data) });
        event.target.reset();
        showToast('Student created successfully.');
        await Promise.all([loadDashboard(), loadStudents()]);
    } catch (error) { showToast(error.message); }
}

async function createCompany(event) {
    event.preventDefault();
    try {
        const data = formDataToObject(event.target);
        await request('/companies', { method: 'POST', body: JSON.stringify(data) });
        event.target.reset();
        showToast('Company added successfully.');
        await Promise.all([loadDashboard(), loadCompanies(), loadJobs()]);
    } catch (error) { showToast(error.message); }
}

async function createInterview(event) {
    event.preventDefault();
    try {
        const data = formDataToObject(event.target);
        data.application_id = Number(data.application_id);
        data.scheduled_at = new Date(data.scheduled_at).toISOString();
        await request('/interviews', { method: 'POST', body: JSON.stringify(data) });
        event.target.reset();
        showToast('Interview scheduled successfully.');
        await loadInterviews();
    } catch (error) { showToast(error.message); }
}

document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', async () => {
        document.querySelectorAll('.tab').forEach(button => button.classList.remove('active'));
        document.querySelectorAll('.section').forEach(section => section.classList.remove('active-section'));
        tab.classList.add('active');
        document.getElementById(tab.dataset.section).classList.add('active-section');
    });
});

$('#searchJobs').addEventListener('click', loadJobs);
$('#jobSearch').addEventListener('keydown', event => { if (event.key === 'Enter') loadJobs(); });
$('#jobLocation').addEventListener('keydown', event => { if (event.key === 'Enter') loadJobs(); });
$('#studentForm').addEventListener('submit', createStudent);
$('#companyForm').addEventListener('submit', createCompany);
$('#interviewForm').addEventListener('submit', createInterview);

(async function init() {
    try {
        await Promise.all([loadDashboard(), loadJobs(), loadStudents(), loadApplications(), loadInterviews(), loadCompanies()]);
    } catch (error) {
        showToast('Backend is not connected. Start FastAPI and refresh the page.');
    }
})();
