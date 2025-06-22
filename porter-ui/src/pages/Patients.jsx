import React, { useState } from 'react';
import { 
  Users, 
  Search, 
  Plus, 
  Filter,
  User,
  MapPin,
  Phone,
  Calendar,
  Activity,
  AlertCircle,
  CheckCircle,
  Clock,
  FileText,
  Pill,
  Heart,
  Thermometer,
  MoreVertical,
  X
} from 'lucide-react';

const Patients = ({ patients }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [selectedPatient, setSelectedPatient] = useState(null);

  const getStatusColor = (status) => {
    switch (status) {
      case 'stable': return '#22c55e';
      case 'critical': return '#ef4444';
      case 'recovering': return '#f59e0b';
      case 'discharged': return '#6b7280';
      default: return '#9ca3af';
    }
  };

  const getRiskColor = (risk) => {
    switch (risk) {
      case 'low': return '#22c55e';
      case 'medium': return '#f59e0b';
      case 'high': return '#ef4444';
      default: return '#6b7280';
    }
  };

  const filteredPatients = patients.filter(patient => {
    const matchesSearch = patient.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         patient.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         patient.room.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         patient.condition.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesFilter = filterStatus === 'all' || patient.status === filterStatus;
    
    return matchesSearch && matchesFilter;
  });

  const PatientCard = ({ patient }) => (
    <div className="patient-card" onClick={() => setSelectedPatient(patient)}>
      <div className="patient-header">
        <div className="patient-info">
          <div className="patient-avatar">
            <User size={24} />
          </div>
          <div className="patient-details">
            <h3>{patient.name}</h3>
            <p className="patient-id">{patient.id}</p>
            <p className="patient-demographics">{patient.age}y • {patient.gender}</p>
          </div>
        </div>
        <div className="patient-status">
          <span 
            className="status-badge"
            style={{ backgroundColor: getStatusColor(patient.status) }}
          >
            {patient.status}
          </span>
          <div 
            className="risk-indicator"
            style={{ backgroundColor: getRiskColor(patient.riskLevel) }}
          >
            {patient.riskLevel} risk
          </div>
        </div>
      </div>

      <div className="patient-location">
        <MapPin size={16} />
        <span>Room {patient.room} - Bed {patient.bed}</span>
      </div>

      <div className="patient-condition">
        <h4>{patient.condition}</h4>
        <p>Attending: {patient.doctor}</p>
      </div>

      <div className="patient-vitals-preview">
        <div className="vital-item">
          <Heart size={16} />
          <span>{patient.vitals.heartRate}</span>
        </div>
        <div className="vital-item">
          <Activity size={16} />
          <span>{patient.vitals.bloodPressure}</span>
        </div>
        <div className="vital-item">
          <Thermometer size={16} />
          <span>{patient.vitals.temperature}</span>
        </div>
      </div>

      <div className="patient-footer">
        <span className="admission-date">
          <Calendar size={14} />
          Admitted {patient.admissionDate}
        </span>
        <button className="icon-button">
          <MoreVertical size={16} />
        </button>
      </div>
    </div>
  );

  const PatientDetail = ({ patient }) => (
    <div className="patient-detail">
      <div className="detail-header">
        <div className="patient-title">
          <h2>{patient.name}</h2>
          <span className="patient-id">{patient.id}</span>
        </div>
        <div className="detail-actions">
          <button className="secondary-button">
            <FileText size={16} />
            View Notes
          </button>
          <button className="secondary-button">
            <Pill size={16} />
            Medications
          </button>
          <button className="primary-button">
            <Plus size={16} />
            New Order
          </button>
          <button className="close-button" onClick={() => setSelectedPatient(null)}>
            <X size={20} />
          </button>
        </div>
      </div>

      <div className="detail-content">
        <div className="detail-section">
          <h3>Patient Information</h3>
          <div className="info-grid">
            <div className="info-item">
              <label>Age/Gender:</label>
              <span>{patient.age} years old, {patient.gender}</span>
            </div>
            <div className="info-item">
              <label>Room/Bed:</label>
              <span>{patient.room} - Bed {patient.bed}</span>
            </div>
            <div className="info-item">
              <label>Admission Date:</label>
              <span>{patient.admissionDate}</span>
            </div>
            <div className="info-item">
              <label>Attending Physician:</label>
              <span>{patient.doctor}</span>
            </div>
            <div className="info-item">
              <label>Primary Condition:</label>
              <span>{patient.condition}</span>
            </div>
            <div className="info-item">
              <label>Status:</label>
              <span style={{ color: getStatusColor(patient.status) }}>
                {patient.status.charAt(0).toUpperCase() + patient.status.slice(1)}
              </span>
            </div>
          </div>
        </div>

        <div className="detail-section">
          <h3>Contact Information</h3>
          <div className="info-grid">
            <div className="info-item">
              <label>Phone:</label>
              <span>{patient.phone}</span>
            </div>
            <div className="info-item">
              <label>Emergency Contact:</label>
              <span>{patient.emergencyContact}</span>
            </div>
            <div className="info-item">
              <label>Insurance:</label>
              <span>{patient.insurance}</span>
            </div>
          </div>
        </div>

        <div className="detail-section">
          <h3>Current Vitals</h3>
          <div className="vitals-grid">
            <div className="vital-card">
              <Activity className="vital-icon" />
              <div className="vital-info">
                <span className="vital-label">Blood Pressure</span>
                <span className="vital-value">{patient.vitals.bloodPressure}</span>
              </div>
            </div>
            <div className="vital-card">
              <Heart className="vital-icon" />
              <div className="vital-info">
                <span className="vital-label">Heart Rate</span>
                <span className="vital-value">{patient.vitals.heartRate}</span>
              </div>
            </div>
            <div className="vital-card">
              <Thermometer className="vital-icon" />
              <div className="vital-info">
                <span className="vital-label">Temperature</span>
                <span className="vital-value">{patient.vitals.temperature}</span>
              </div>
            </div>
            <div className="vital-card">
              <Activity className="vital-icon" />
              <div className="vital-info">
                <span className="vital-label">Oxygen Sat</span>
                <span className="vital-value">{patient.vitals.oxygenSat}</span>
              </div>
            </div>
          </div>
          <p className="vital-timestamp">
            <Clock size={14} />
            Last updated: {patient.vitals.lastUpdated}
          </p>
        </div>

        <div className="detail-section">
          <h3>Medications</h3>
          <div className="medication-list">
            {patient.medications.map((medication, index) => (
              <div key={index} className="medication-item">
                <Pill size={16} />
                <span>{medication}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="detail-section">
          <h3>Allergies</h3>
          <div className="allergy-list">
            {patient.allergies.map((allergy, index) => (
              <span key={index} className="allergy-tag">
                <AlertCircle size={14} />
                {allergy}
              </span>
            ))}
          </div>
        </div>

        <div className="detail-section">
          <h3>Clinical Notes</h3>
          <div className="notes-content">
            <p>{patient.notes}</p>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="patients-container">
      <div className="patients-header">
        <div className="page-title">
          <Users size={28} />
          <h1>Patients</h1>
        </div>
        <div className="header-actions">
          <button className="primary-button">
            <Plus size={16} />
            Add Patient
          </button>
        </div>
      </div>

      <div className="patients-filters">
        <div className="search-box">
          <Search className="search-icon" size={16} />
          <input
            type="text"
            placeholder="Search patients by name, ID, room, or condition..."
            className="search-input"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <select
          className="filter-select"
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
        >
          <option value="all">All Statuses</option>
          <option value="stable">Stable</option>
          <option value="critical">Critical</option>
          <option value="recovering">Recovering</option>
          <option value="discharged">Discharged</option>
        </select>
      </div>

      <div className="patients-grid">
        {filteredPatients.map(patient => (
          <PatientCard key={patient.id} patient={patient} />
        ))}
      </div>

      {filteredPatients.length === 0 && (
        <div style={{ 
          textAlign: 'center', 
          padding: '40px', 
          color: '#64748b',
          borderRadius: '12px',
          border: '1px solid #e2e8f0'
        }}>
          <Users size={48} style={{ marginBottom: '16px', opacity: 0.5 }} />
          <p>No patients found matching your search criteria.</p>
        </div>
      )}

      {selectedPatient && <PatientDetail patient={selectedPatient} />}
    </div>
  );
};

export default Patients;