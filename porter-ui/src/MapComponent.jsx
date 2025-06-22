import React, { useEffect, useState, useRef, useCallback } from 'react';

// Physics simulation class for cleaner separation of concerns
class ForceSimulation {
  constructor(nodes, connections, config = {}) {
    this.config = {
      nodeRadius: 15,
      repulsionStrength: 2000,
      attractionStrength: 0.08,
      dampingFactor: 0.85,
      idealDistance: 120,
      centeringForce: 0.001,
      minVelocity: 0.1,
      maxVelocity: 10,
      width: 800,
      height: 600,
      ...config
    };

    this.nodes = new Map();
    this.connections = connections;
    this.isRunning = false;
    this.animationFrame = null;

    // Initialize nodes with random positions
    this.initializeNodes(nodes);
  }

  initializeNodes(nodes) {
    const { width, height, nodeRadius } = this.config;
    
    nodes.forEach(node => {
      this.nodes.set(node.id, {
        ...node,
        x: Math.random() * (width - 2 * nodeRadius) + nodeRadius,
        y: Math.random() * (height - 2 * nodeRadius) + nodeRadius,
        vx: 0,
        vy: 0,
        fx: 0, // Force accumulator
        fy: 0
      });
    });
  }

  calculateForces() {
    const { repulsionStrength, attractionStrength, idealDistance, centeringForce, width, height } = this.config;
    
    // Reset forces
    for (const node of this.nodes.values()) {
      node.fx = 0;
      node.fy = 0;
    }

    // Repulsive forces between all nodes
    const nodeArray = Array.from(this.nodes.values());
    for (let i = 0; i < nodeArray.length; i++) {
      for (let j = i + 1; j < nodeArray.length; j++) {
        const nodeA = nodeArray[i];
        const nodeB = nodeArray[j];
        
        const dx = nodeB.x - nodeA.x;
        const dy = nodeB.y - nodeA.y;
        const distanceSquared = dx * dx + dy * dy;
        
        if (distanceSquared === 0) continue;
        
        const distance = Math.sqrt(distanceSquared);
        const force = repulsionStrength / distanceSquared;
        const fx = force * (dx / distance);
        const fy = force * (dy / distance);
        
        nodeA.fx -= fx;
        nodeA.fy -= fy;
        nodeB.fx += fx;
        nodeB.fy += fy;
      }
    }

    // Attractive forces for connected nodes
    this.connections.forEach(connection => {
      const nodeA = this.nodes.get(connection.node_a);
      const nodeB = this.nodes.get(connection.node_b);
      
      if (!nodeA || !nodeB) return;
      
      const dx = nodeB.x - nodeA.x;
      const dy = nodeB.y - nodeA.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance === 0) return;
      
      const force = attractionStrength * (distance - idealDistance);
      const fx = force * (dx / distance);
      const fy = force * (dy / distance);
      
      nodeA.fx += fx;
      nodeA.fy += fy;
      nodeB.fx -= fx;
      nodeB.fy -= fy;
    });

    // Centering force to prevent nodes from drifting away
    const centerX = width / 2;
    const centerY = height / 2;
    
    for (const node of this.nodes.values()) {
      node.fx += (centerX - node.x) * centeringForce;
      node.fy += (centerY - node.y) * centeringForce;
    }
  }

  updatePositions() {
    const { dampingFactor, minVelocity, maxVelocity, nodeRadius, width, height } = this.config;
    let maxMovement = 0;

    for (const node of this.nodes.values()) {
      // Update velocities with damping
      node.vx = (node.vx + node.fx) * dampingFactor;
      node.vy = (node.vy + node.fy) * dampingFactor;
      
      // Clamp velocities
      node.vx = Math.max(-maxVelocity, Math.min(maxVelocity, node.vx));
      node.vy = Math.max(-maxVelocity, Math.min(maxVelocity, node.vy));
      
      // Update positions
      node.x += node.vx;
      node.y += node.vy;
      
      // Keep nodes within bounds
      node.x = Math.max(nodeRadius, Math.min(width - nodeRadius, node.x));
      node.y = Math.max(nodeRadius, Math.min(height - nodeRadius, node.y));
      
      // Track maximum movement for convergence detection
      maxMovement = Math.max(maxMovement, Math.abs(node.vx), Math.abs(node.vy));
    }

    return maxMovement;
  }

  tick() {
    this.calculateForces();
    const maxMovement = this.updatePositions();
    return maxMovement > this.config.minVelocity;
  }

  start(onUpdate) {
    if (this.isRunning) return;
    
    this.isRunning = true;
    
    const animate = () => {
      if (!this.isRunning) return;
      
      const shouldContinue = this.tick();
      onUpdate(this.getNodePositions());
      
      if (shouldContinue) {
        this.animationFrame = requestAnimationFrame(animate);
      } else {
        this.isRunning = false;
        console.log('Simulation converged');
      }
    };
    
    animate();
  }

  stop() {
    this.isRunning = false;
    if (this.animationFrame) {
      cancelAnimationFrame(this.animationFrame);
    }
  }

  getNodePositions() {
    const positions = {};
    for (const [id, node] of this.nodes) {
      positions[id] = { x: node.x, y: node.y };
    }
    return positions;
  }
}

// Custom hook for managing the simulation
const useForceSimulation = (graph) => {
  const [nodePositions, setNodePositions] = useState({});
  const [isSimulating, setIsSimulating] = useState(false);
  const simulationRef = useRef(null);

  const startSimulation = useCallback(() => {
    if (!graph || simulationRef.current) return;

    setIsSimulating(true);
    
    const simulation = new ForceSimulation(graph.nodes, graph.connections);
    simulationRef.current = simulation;

    const handleUpdate = (positions) => {
      setNodePositions(positions);
    };

    simulation.start(handleUpdate);
    
    // Auto-stop after reasonable time if not converged
    setTimeout(() => {
      if (simulation.isRunning) {
        simulation.stop();
        setIsSimulating(false);
      }
    }, 10000);

  }, [graph]);

  const stopSimulation = useCallback(() => {
    if (simulationRef.current) {
      simulationRef.current.stop();
      simulationRef.current = null;
      setIsSimulating(false);
    }
  }, []);

  useEffect(() => {
    if (graph) {
      startSimulation();
    }
    
    return () => {
      stopSimulation();
    };
  }, [graph, startSimulation, stopSimulation]);

  return { nodePositions, isSimulating, startSimulation, stopSimulation };
};

// Bot Info Popup Component
const BotInfoPopup = ({ bot, position, onClose }) => {
  const statusColors = {
    active: '#22c55e',
    idle: '#f59e0b',
    offline: '#ef4444',
    maintenance: '#8b5cf6'
  };

  const statusBgs = {
    active: 'rgba(34, 197, 94, 0.1)',
    idle: 'rgba(245, 158, 11, 0.1)',
    offline: 'rgba(239, 68, 68, 0.1)',
    maintenance: 'rgba(139, 92, 246, 0.1)'
  };

  return (
    <div
      style={{
        position: 'absolute',
        left: position.x + 20,
        top: position.y - 10,
        background: 'rgba(15, 23, 42, 0.95)',
        backdropFilter: 'blur(12px)',
        border: '1px solid rgba(51, 65, 85, 0.5)',
        borderRadius: '8px',
        padding: '12px',
        minWidth: '200px',
        zIndex: 1000,
        fontSize: '12px',
        color: '#e2e8f0',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
        transform: 'translateY(-50%)',
        pointerEvents: 'auto'
      }}
      onClick={(e) => e.stopPropagation()}
    >
      {/* Close button */}
      <button
        onClick={onClose}
        style={{
          position: 'absolute',
          top: '4px',
          right: '4px',
          background: 'transparent',
          border: 'none',
          color: '#94a3b8',
          cursor: 'pointer',
          fontSize: '16px',
          padding: '2px',
          borderRadius: '4px'
        }}
        onMouseEnter={(e) => e.target.style.background = 'rgba(51, 65, 85, 0.5)'}
        onMouseLeave={(e) => e.target.style.background = 'transparent'}
      >
        ×
      </button>

      {/* Bot Header */}
      <div style={{ marginBottom: '8px', paddingRight: '16px' }}>
        <div style={{ 
          fontWeight: '600', 
          fontSize: '14px', 
          marginBottom: '4px',
          color: '#f1f5f9'
        }}>
          {bot.name}
        </div>
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '6px',
          marginBottom: '6px'
        }}>
          <div
            style={{
              width: '8px',
              height: '8px',
              borderRadius: '50%',
              backgroundColor: statusColors[bot.status] || statusColors.offline,
              boxShadow: `0 0 8px ${statusColors[bot.status] || statusColors.offline}`
            }}
          />
          <span style={{ 
            color: statusColors[bot.status] || statusColors.offline,
            fontWeight: '500',
            textTransform: 'capitalize'
          }}>
            {bot.status}
          </span>
        </div>
      </div>

      {/* Bot Details */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <span style={{ color: '#94a3b8' }}>Battery:</span>
          <span style={{ 
            color: bot.battery > 20 ? '#22c55e' : '#ef4444',
            fontWeight: '500'
          }}>
            {bot.battery}%
          </span>
        </div>
        
        {bot.task && (
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: '#94a3b8' }}>Task:</span>
            <span style={{ 
              color: '#e2e8f0',
              fontSize: '11px',
              textAlign: 'right',
              maxWidth: '120px',
              wordWrap: 'break-word'
            }}>
              {bot.task}
            </span>
          </div>
        )}

        {bot.priority && (
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: '#94a3b8' }}>Priority:</span>
            <span style={{ 
              color: bot.priority === 'critical' ? '#ef4444' : 
                     bot.priority === 'high' ? '#f97316' : 
                     bot.priority === 'normal' ? '#3b82f6' : '#6b7280',
              fontWeight: '500',
              textTransform: 'capitalize'
            }}>
              {bot.priority}
            </span>
          </div>
        )}

        <div style={{ 
          marginTop: '8px',
          padding: '6px 8px',
          background: statusBgs[bot.status] || statusBgs.offline,
          borderRadius: '4px',
          border: `1px solid ${statusColors[bot.status] || statusColors.offline}40`
        }}>
          <div style={{ fontSize: '10px', color: '#94a3b8', marginBottom: '2px' }}>
            Location
          </div>
          <div style={{ fontSize: '11px', fontWeight: '500' }}>
            {bot.location}
          </div>
        </div>
      </div>
    </div>
  );
};

// Main component
const MapComponent = ({ bots = [] }) => {
  const [graph, setGraph] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedBot, setSelectedBot] = useState(null);
  const [hoveredNode, setHoveredNode] = useState(null);
  
  const { nodePositions, isSimulating } = useForceSimulation(graph);

  const baseURL = import.meta.env.VITE_API_BASE_URL;

  useEffect(() => {
    const fetchGraph = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${baseURL}/api/graph`);
        
        if (!response.ok) {
          throw new Error(`Failed to fetch graph: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (!data.nodes || !data.connections) {
          throw new Error('Invalid graph data structure');
        }
        
        setGraph(data);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch graph data:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchGraph();
  }, [baseURL]);

  const renderConnections = () => {
    if (!graph?.connections) return null;

    return graph.connections.map((connection, index) => {
      const nodeA = nodePositions[connection.node_a];
      const nodeB = nodePositions[connection.node_b];

      if (!nodeA || !nodeB) return null;

      return (
        <line
          key={`connection-${connection.node_a}-${connection.node_b}-${index}`}
          x1={nodeA.x}
          y1={nodeA.y}
          x2={nodeB.x}
          y2={nodeB.y}
          stroke="url(#connectionGradient)"
          strokeWidth="1.5"
          strokeOpacity="0.8"
          style={{
            filter: 'drop-shadow(0px 0px 2px rgba(148, 163, 184, 0.4))'
          }}
        />
      );
    });
  };

  const getBotsAtLocation = (nodeName) => {
    return bots.filter(bot => bot.location === nodeName);
  };

  const renderNodes = () => {
    if (!graph?.nodes) return null;

    return graph.nodes.map(node => {
      const position = nodePositions[node.id];
      const botsAtLocation = getBotsAtLocation(node.name);
      const hasActiveBots = botsAtLocation.some(bot => bot.status === 'active');
      const isHovered = hoveredNode === node.id;
      
      if (!position) return null;

      return (
        <g key={`node-${node.id}`}>
          {/* Node glow effect when bots are present */}
          {botsAtLocation.length > 0 && (
            <circle
              cx={position.x}
              cy={position.y}
              r="24"
              fill="none"
              stroke={hasActiveBots ? "#22c55e" : "#f59e0b"}
              strokeWidth="2"
              strokeOpacity="0.3"
              style={{
                animation: hasActiveBots ? 'pulse 2s infinite' : 'none'
              }}
            />
          )}
          
          {/* Main node */}
          <circle
            cx={position.x}
            cy={position.y}
            r={isHovered ? "18" : "16"}
            fill={botsAtLocation.length > 0 ? "rgba(59, 130, 246, 0.5)" : "rgba(59, 130, 246, 0.3)"}
            stroke="#3b82f6"
            strokeWidth="2"
            filter="url(#glow)"
            style={{
              cursor: 'pointer',
              transition: 'all 0.3s ease'
            }}
            onMouseEnter={() => setHoveredNode(node.id)}
            onMouseLeave={() => setHoveredNode(null)}
            onClick={() => {
              if (botsAtLocation.length > 0) {
                setSelectedBot(selectedBot ? null : botsAtLocation[0]);
              }
            }}
          />
          
          {/* Bot count indicator */}
          {botsAtLocation.length > 0 && (
            <g>
              <circle
                cx={position.x + 12}
                cy={position.y - 12}
                r="8"
                fill="rgba(15, 23, 42, 0.9)"
                stroke="#3b82f6"
                strokeWidth="1.5"
              />
              <text
                x={position.x + 12}
                y={position.y - 8}
                textAnchor="middle"
                fontSize="10"
                fill="#60a5fa"
                fontWeight="600"
                style={{ pointerEvents: 'none' }}
              >
                {botsAtLocation.length}
              </text>
            </g>
          )}
          
          {/* Node label */}
          <text
            x={position.x}
            y={position.y + (botsAtLocation.length > 0 ? 36 : 32)}
            textAnchor="middle"
            fontSize="11"
            fill="#cbd5e1"
            fontWeight="500"
            style={{
              pointerEvents: 'none',
              userSelect: 'none',
              textShadow: '0 1px 2px rgba(0, 0, 0, 0.8)'
            }}
          >
            {node.name}
          </text>
        </g>
      );
    });
  };

  const renderBotPopups = () => {
    if (!selectedBot || !graph?.nodes) return null;

    const botNode = graph.nodes.find(node => node.name === selectedBot.location);
    const position = botNode ? nodePositions[botNode.id] : null;
    
    if (!position) return null;

    return (
      <BotInfoPopup
        bot={selectedBot}
        position={position}
        onClose={() => setSelectedBot(null)}
      />
    );
  };

  if (loading) {
    return (
      <div className="panel" style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '500px'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{
            width: '48px',
            height: '48px',
            border: '3px solid rgba(100, 116, 139, 0.3)',
            borderTop: '3px solid #3b82f6',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            margin: '0 auto 1rem'
          }}></div>
          <p style={{ color: '#94a3b8' }}>Loading map data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="panel" style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '500px',
        background: 'rgba(239, 68, 68, 0.1)',
        border: '1px solid rgba(239, 68, 68, 0.3)'
      }}>
        <div style={{ textAlign: 'center' }}>
          <p style={{ color: '#f87171', fontWeight: '500', marginBottom: '0.5rem' }}>Failed to load map</p>
          <p style={{ color: '#fca5a5', fontSize: '0.875rem' }}>{error}</p>
        </div>
      </div>
    );
  }

  if (!graph || Object.keys(nodePositions).length === 0) {
    return (
      <div className="panel" style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '500px'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ marginBottom: '1rem' }}>
            <div style={{
              height: '1rem',
              background: 'rgba(100, 116, 139, 0.3)',
              borderRadius: '0.25rem',
              width: '12rem',
              margin: '0 auto 0.5rem',
              animation: 'pulse 1.5s infinite'
            }}></div>
            <div style={{
              height: '1rem',
              background: 'rgba(100, 116, 139, 0.3)',
              borderRadius: '0.25rem',
              width: '8rem',
              margin: '0 auto'
            }}></div>
          </div>
          <p style={{ color: '#94a3b8', marginTop: '1rem' }}>Arranging layout...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="panel">
      {isSimulating && (
        <div style={{
          background: 'rgba(59, 130, 246, 0.2)',
          borderBottom: '1px solid rgba(59, 130, 246, 0.3)',
          padding: '0.75rem 1.5rem',
          marginBottom: '1rem',
          borderRadius: '0.5rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          color: '#60a5fa',
          fontSize: '0.875rem'
        }}>
          <div style={{
            width: '16px',
            height: '16px',
            border: '2px solid transparent',
            borderTop: '2px solid #60a5fa',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite'
          }}></div>
          Optimizing layout...
        </div>
      )}
      
      <div style={{
        width: '100%',
        height: '500px',
        background: 'rgba(15, 23, 42, 0.5)',
        backdropFilter: 'blur(12px)',
        border: '1px solid rgba(51, 65, 85, 0.3)',
        borderRadius: '0.75rem',
        overflow: 'hidden',
        position: 'relative'
      }}
      onClick={() => setSelectedBot(null)} // Close popup when clicking on map
      >
        <svg 
          viewBox="0 0 800 600" 
          style={{
            width: '100%',
            height: '100%',
            background: 'linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.8) 50%, rgba(15, 23, 42, 0.8) 100%)'
          }}
        >
          <defs>
            <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
              <feMerge> 
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
            <linearGradient id="connectionGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="rgba(100, 116, 139, 0.6)"/>
              <stop offset="50%" stopColor="rgba(148, 163, 184, 0.8)"/>
              <stop offset="100%" stopColor="rgba(100, 116, 139, 0.6)"/>
            </linearGradient>
          </defs>
          
          {renderConnections()}
          {renderNodes()}
        </svg>

        {/* Bot Info Popups */}
        {renderBotPopups()}

        <style jsx>{`
          @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }
          @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(1.1); }
          }
        `}</style>
      </div>

      {/* Legend */}
      <div style={{
        marginTop: '1rem',
        display: 'flex',
        flexWrap: 'wrap',
        gap: '1rem',
        fontSize: '0.75rem'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#cbd5e1' }}>
          <div style={{
            width: '12px',
            height: '12px',
            borderRadius: '50%',
            background: 'rgba(59, 130, 246, 0.5)',
            border: '1px solid #3b82f6'
          }}></div>
          <span>Node with bots</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#cbd5e1' }}>
          <div style={{
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            background: '#22c55e',
            boxShadow: '0 0 8px rgba(34, 197, 94, 0.6)'
          }}></div>
          <span>Active Bot</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#cbd5e1' }}>
          <div style={{
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            background: '#f59e0b',
            boxShadow: '0 0 8px rgba(245, 158, 11, 0.6)'
          }}></div>
          <span>Idle Bot</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#cbd5e1' }}>
          <div style={{
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            background: '#ef4444',
            boxShadow: '0 0 8px rgba(239, 68, 68, 0.6)'
          }}></div>
          <span>Offline Bot</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#cbd5e1' }}>
          <div style={{
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            background: '#8b5cf6',
            boxShadow: '0 0 8px rgba(139, 92, 246, 0.6)'
          }}></div>
          <span>Maintenance</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#94a3b8', fontSize: '0.7rem' }}>
          <span>💡 Click nodes with bots to see details</span>
        </div>
      </div>
    </div>
  );
};

export default MapComponent;