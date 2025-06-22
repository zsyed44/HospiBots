import React, { useState } from 'react';
import { 
  FileText, 
  Mic, 
  MicOff, 
  Save, 
  Search, 
  Plus,
  User,
  Calendar,
  Clock,
  Tag,
  Edit3,
  Trash2,
  Download,
  Filter
} from 'lucide-react';

const Scribing = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [activeNote, setActiveNote] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [noteContent, setNoteContent] = useState('');
  const [selectedTemplate, setSelectedTemplate] = useState('');

  // Mock notes data
  const [notes] = useState([
    {
      id: 1,
      title: 'Patient Consultation - Sarah Johnson',
      patient: 'Sarah Johnson (P-2024-001)',
      room: '301A',
      date: '2024-06-22',
      time: '14:30',
      type: 'consultation',
      status: 'completed',
      content: 'Patient presents with mild hypertension. Blood pressure readings: 145/90. Discussed lifestyle modifications including diet and exercise. Prescribed Lisinopril 10mg daily. Follow-up in 2 weeks.',
      tags: ['hypertension', 'follow-up', 'medication'],
      createdBy: 'Dr. Smith',
      duration: '15 min'
    },
    {
      id: 2,
      title: 'Rounds Notes - ICU Ward',
      patient: 'Multiple Patients',
      room: 'ICU',
      date: '2024-06-22',
      time: '08:00',
      type: 'rounds',
      status: 'draft',
      content: 'Morning rounds completed. Room 101: Patient stable, vitals improving. Room 102: Requires additional monitoring. Room 103: Ready for discharge planning.',
      tags: ['rounds', 'ICU', 'vitals'],
      createdBy: 'Dr. Williams',
      duration: '45 min'
    },
    {
      id: 3,
      title: 'Emergency Assessment - Michael Chen',
      patient: 'Michael Chen (P-2024-002)',
      room: '205B',
      date: '2024-06-21',
      time: '22:15',
      type: 'emergency',
      status: 'completed',
      content: 'Patient admitted with chest pain. EKG normal, troponins negative. Observation for 24 hours. Cardiology consult requested.',
      tags: ['emergency', 'chest-pain', 'cardiology'],
      createdBy: 'Dr. Johnson',
      duration: '30 min'
    }
  ]);

  const templates = [
    { id: 'consultation', name: 'Patient Consultation', content: 'Chief Complaint:\n\nHistory of Present Illness:\n\nPhysical Examination:\n\nAssessment:\n\nPlan:' },
    { id: 'discharge', name: 'Discharge Summary', content: 'Admission Date:\nDischarge Date:\n\nDiagnosis:\n\nHospital Course:\n\nDischarge Medications:\n\nFollow-up Instructions:' },
    { id: 'progress', name: 'Progress Note', content: 'Subjective:\n\nObjective:\n\nAssessment:\n\nPlan:' },
    { id: 'procedure', name: 'Procedure Note', content: 'Procedure:\nIndication:\nTechnique:\nComplications:\nPost-procedure Status:' }
  ];

  const getTypeColor = (type) => {
    switch (type) {
      case 'consultation': return '#3b82f6';
      case 'rounds': return '#22c55e';
      case 'emergency': return '#ef4444';
      case 'progress': return '#f59e0b';
      case 'discharge': return '#8b5cf6';
      default: return '#6b7280';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return '#22c55e';
      case 'draft': return '#f59e0b';
      case 'review': return '#3b82f6';
      default: return '#6b7280';
    }
  };

  const filteredNotes = notes.filter(note =>
    note.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    note.patient.toLowerCase().includes(searchTerm.toLowerCase()) ||
    note.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const NoteCard = ({ note }) => (
    <div className="note-card" onClick={() => setActiveNote(note)}>
      <div className="note-header">
        <div className="note-title">
          <h3>{note.title}</h3>
          <div className="note-meta">
            <span className="note-type" style={{ color: getTypeColor(note.type) }}>
              {note.type}
            </span>
            <span className="note-status" style={{ color: getStatusColor(note.status) }}>
              {note.status}
            </span>
          </div>
        </div>
        <div className="note-actions">
          <button className="icon-button">
            <Edit3 size={16} />
          </button>
          <button className="icon-button">
            <Download size={16} />
          </button>
          <button className="icon-button">
            <Trash2 size={16} />
          </button>
        </div>
      </div>

      <div className="note-info">
        <div className="note-detail">
          <User size={16} />
          <span>{note.patient}</span>
        </div>
        <div className="note-detail">
          <Calendar size={16} />
          <span>{note.date} at {note.time}</span>
        </div>
        <div className="note-detail">
          <Clock size={16} />
          <span>{note.duration}</span>
        </div>
      </div>

      <div className="note-preview">
        <p>{note.content.substring(0, 150)}...</p>
      </div>

      <div className="note-tags">
        {note.tags.map(tag => (
          <span key={tag} className="note-tag">
            <Tag size={12} />
            {tag}
          </span>
        ))}
      </div>
    </div>
  );

  const NoteEditor = () => (
    <div className="note-editor">
      <div className="editor-header">
        <h2>{activeNote ? `Edit: ${activeNote.title}` : 'New Note'}</h2>
        <div className="editor-actions">
          <div className="recording-controls">
            <button
              onClick={() => setIsRecording(!isRecording)}
              className={`recording-button ${isRecording ? 'recording' : ''}`}
            >
              {isRecording ? <MicOff size={20} /> : <Mic size={20} />}
              {isRecording ? 'Stop Recording' : 'Start Recording'}
            </button>
          </div>
          <button className="secondary-button">
            Save Draft
          </button>
          <button className="primary-button">
            <Save size={16} />
            Complete Note
          </button>
        </div>
      </div>

      <div className="editor-controls">
        <select 
          value={selectedTemplate} 
          onChange={(e) => setSelectedTemplate(e.target.value)}
          className="template-select"
        >
          <option value="">Select Template</option>
          {templates.map(template => (
            <option key={template.id} value={template.id}>
              {template.name}
            </option>
          ))}
        </select>
        
        <div className="note-metadata">
          <input type="text" placeholder="Patient Name" className="metadata-input" />
          <input type="text" placeholder="Room Number" className="metadata-input" />
          <select className="metadata-select">
            <option value="consultation">Consultation</option>
            <option value="rounds">Rounds</option>
            <option value="emergency">Emergency</option>
            <option value="progress">Progress</option>
            <option value="discharge">Discharge</option>
          </select>
        </div>
      </div>

      <div className="editor-content">
        <textarea
          value={noteContent || (activeNote ? activeNote.content : '')}
          onChange={(e) => setNoteContent(e.target.value)}
          placeholder="Start typing your note or use voice recording..."
          className="note-textarea"
        />
      </div>

      {isRecording && (
        <div className="recording-indicator">
          <div className="recording-animation"></div>
          <span>Recording in progress... Speak clearly into your microphone</span>
        </div>
      )}
    </div>
  );

  return (
    <div className="page">
      <div className="page-header">
        <h1>Clinical Notes & Scribing</h1>
        <div className="page-actions">
          <button className="secondary-button">
            <Filter size={16} />
            Filter
          </button>
          <button 
            className="primary-button"
            onClick={() => setActiveNote(null)}
          >
            <Plus size={16} />
            New Note
          </button>
        </div>
      </div>

      <div className="scribing-layout">
        <div className="notes-sidebar">
          <div className="sidebar-header">
            <div className="search-box">
              <Search size={16} />
              <input 
                type="text" 
                placeholder="Search notes..." 
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>

          <div className="notes-list">
            {filteredNotes.map(note => (
              <NoteCard key={note.id} note={note} />
            ))}
          </div>
        </div>

        <div className="editor-main">
          {activeNote !== null || noteContent ? (
            <NoteEditor />
          ) : (
            <div className="editor-placeholder">
              <FileText size={64} />
              <h3>Select a note to edit or create a new one</h3>
              <p>Use voice recording for hands-free documentation</p>
              <button 
                className="primary-button"
                onClick={() => setActiveNote({})}
              >
                <Plus size={16} />
                Start New Note
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Scribing;