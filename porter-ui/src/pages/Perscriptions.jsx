import React, { useState } from 'react';
import { 
  Plus, 
  Search, 
  Filter, 
  Pill, 
  User, 
  Clock, 
  AlertTriangle,
  CheckCircle,
  MoreVertical,
  Calendar,
  MapPin
} from 'lucide-react';

const Prescriptions = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');

  // Mock prescription data
  const [prescriptions] = useState([
    {
      id: 1,
      patientName: 'Sarah Johnson',
      patientId: 'P-2024-001',
      room: '301A',
      medication: 'Lisinopril 10mg',
      dosage: '1 tablet daily',
      frequency: 'Once daily',
      startDate: '2024-06-20',
      endDate: '2024-07-20',
      status: 'active',
      prescribedBy: 'Dr. Smith',
      priority: 'normal',
      lastDispensed: '2024-06-22 08:00',
      nextDue: '2024-06-23 08:00',
      instructions: 'Take with food'
    },
    {
      id: 2,
      patientName: 'Michael Chen',
      patientId: 'P-2024-002',
      room: '205B',
      medication: 'Metformin 500mg',
      dosage: '2 tablets twice daily',
      frequency: 'Twice daily',
      startDate: '2024-06-18',
      endDate: '2024-07-18',
      status: 'overdue',
      prescribedBy: 'Dr. Williams',
      priority: 'high',
      lastDispensed: '2024-06-21 20:00',
      nextDue: '2024-06-22 08:00',
      instructions: 'Take 30 minutes before meals'
    },
    {
      id: 3,
      patientName: 'Emma Davis',
      patientId: 'P-2024-003',
      room: '412C',
      medication: 'Amoxicillin 250mg',
      dosage: '1 capsule every 8 hours',
      frequency: 'Three times daily',
      startDate: '2024-06-21',
      endDate: '2024-06-28',
      status: 'pending',
      prescribedBy: 'Dr. Johnson',
      priority: 'normal',
      lastDispensed: null,
      nextDue: '2024-06-23 06:00',
      instructions: 'Complete full course even if feeling better'
    },
    {
      id: 4,
      patientName: 'Robert Wilson',
      patientId: 'P-2024-004',
      room: '108A',
      medication: 'Morphine 5mg',
      dosage: '1 tablet as needed',
      frequency: 'PRN for pain',
      startDate: '2024-06-22',
      endDate: '2024-06-25',
      status: 'active',
      prescribedBy: 'Dr. Brown',
      priority: 'critical',
      lastDispensed: '2024-06-22 14:30',
      nextDue: 'As needed',
      instructions: 'Maximum 6 doses per 24 hours'
    }
  ]);

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return '#22c55e';
      case 'overdue': return '#ef4444';
      case 'pending': return '#f59e0b';
      case 'completed': return '#6b7280';
      default: return '#9ca3af';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'critical': return '#ef4444';
      case 'high': return '#f97316';
      case 'normal': return '#3b82f6';
      case 'low': return '#6b7280';
      default: return '#9ca3af';
    }
  };

  const filteredPrescriptions = prescriptions.filter(prescription => {
    const matchesSearch = prescription.patientName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         prescription.medication.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         prescription.room.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesFilter = filterStatus === 'all' || prescription.status === filterStatus;
    
    return matchesSearch && matchesFilter;
  });

  const PrescriptionCard = ({ prescription }) => (
    <div className="prescription-card">
      <div className="prescription-header">
        <div className="prescription-patient">
          <div className="patient-info">
            <h3>{prescription.patientName}</h3>
            <p className="patient-id">{prescription.patientId}</p>
          </div>
          <div className="room-info">
            <MapPin size={16} />
            <span>Room {prescription.room}</span>
          </div>
        </div>
        <div className="prescription-actions">
          <span 
            className="prescription-status"
            style={{ backgroundColor: getStatusColor(prescription.status) }}
          >
            {prescription.status}
          </span>
          <button className="icon-button">
            <MoreVertical size={16} />
          </button>
        </div>
      </div>

      <div className="prescription-medication">
        <div className="medication-info">
          <div className="medication-name">
            <Pill size={20} style={{ color: getPriorityColor(prescription.priority) }} />
            <div>
              <h4>{prescription.medication}</h4>
              <p>{prescription.dosage} - {prescription.frequency}</p>
            </div>
          </div>
          <div className="priority-indicator">
            <div 
              className="priority-dot"
              style={{ backgroundColor: getPriorityColor(prescription.priority) }}
            ></div>
            <span>{prescription.priority}</span>
          </div>
        </div>
      </div>

      <div className="prescription-details">
        <div className="detail-item">
          <User size={16} />
          <span>Prescribed by {prescription.prescribedBy}</span>
        </div>
        <div className="detail-item">
          <Calendar size={16} />
          <span>{prescription.startDate} to {prescription.endDate}</span>
        </div>
        <div className="detail-item">
          <Clock size={16} />
          <span>Next due: {prescription.nextDue}</span>
        </div>
      </div>

      {prescription.instructions && (
        <div className="prescription-instructions">
          <p><strong>Instructions:</strong> {prescription.instructions}</p>
        </div>
      )}

      <div className="prescription-footer">
        <button className="secondary-button">
          <Clock size={16} />
          View History
        </button>
        <button className="primary-button">
          <CheckCircle size={16} />
          Mark Dispensed
        </button>
      </div>
    </div>
  );

  return (
    <div className="page">
      <div className="page-header">
        <h1>Prescription Management</h1>
        <div className="page-actions">
          <button className="secondary-button">
            <Filter size={16} />
            Filter
          </button>
          <button className="primary-button">
            <Plus size={16} />
            New Prescription
          </button>
        </div>
      </div>

      <div className="page-controls">
        <div className="search-box">
          <Search size={16} />
          <input 
            type="text" 
            placeholder="Search prescriptions, patients, or medications..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        
        <div className="filter-tabs">
          {['all', 'active', 'overdue', 'pending', 'completed'].map(status => (
            <button
              key={status}
              onClick={() => setFilterStatus(status)}
              className={`filter-tab ${filterStatus === status ? 'active' : ''}`}
            >
              {status.charAt(0).toUpperCase() + status.slice(1)}
              {status === 'overdue' && <AlertTriangle size={14} style={{ marginLeft: '4px', color: '#ef4444' }} />}
            </button>
          ))}
        </div>
      </div>

      <div className="prescriptions-grid">
        {filteredPrescriptions.map(prescription => (
          <PrescriptionCard key={prescription.id} prescription={prescription} />
        ))}
      </div>

      {filteredPrescriptions.length === 0 && (
        <div className="empty-state">
          <Pill size={64} />
          <h3>No prescriptions found</h3>
          <p>Try adjusting your search or filter criteria</p>
        </div>
      )}
    </div>
  );
};

export default Prescriptions;