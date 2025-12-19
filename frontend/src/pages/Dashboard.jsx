import React, { useState, useRef, useEffect } from 'react';
import api from '../api';

const Dashboard = () => {
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    // State
    const [prompt, setPrompt] = useState('');
    const [selfImage, setSelfImage] = useState(null);
    const [targetImage, setTargetImage] = useState(null);
    const [loading, setLoading] = useState(false);
    const [outputImage, setOutputImage] = useState(null);
    const [history, setHistory] = useState([]);

    const selfInputRef = useRef(null);
    const targetInputRef = useRef(null);

    // Fetch History
    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const res = await api.get('/image/history');
            setHistory(res.data);
        } catch (error) {
            console.error("Failed to load history", error);
        }
    };

    const handleLogout = () => {
        localStorage.clear();
        window.location.href = '/';
    };

    const handleFileChange = (e, setFile) => {
        if (e.target.files && e.target.files[0]) {
            const selectedFile = e.target.files[0];
            const MAX_SIZE = 10 * 1024 * 1024;
            if (selectedFile.size > MAX_SIZE) {
                alert("File is too large! Please upload an image under 10MB.");
                
                // Clear the input value so they can try again
                e.target.value = null; 
                return;
            }
            setFile(selectedFile);
        }
    };

    const handleGenerate = async () => {
        // 1. SelfImage mandatory
        if (!selfImage) {
            alert("Self Image is required! Please upload your photo.");
            return;
        }

        // 2. Conditional Check: At least one of Prompt OR Target Image must exist
        if (!prompt && !targetImage) {
            alert("Please provide at least a Text Prompt OR a Target Style Image.");
            return;
        }

        setLoading(true);
        const formData = new FormData();

        // Append mandatory field
        formData.append('self_image', selfImage);

        // Append optional fields only if they exist
        if (prompt) formData.append('prompt', prompt);
        if (targetImage) formData.append('target_image', targetImage);

        try {
            const res = await api.post('/image/create', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            setOutputImage(res.data.output_url);
            fetchHistory(); // Refresh history list
        } catch (error) {
            console.error("Generation failed", error);
            alert("Generation failed. Check console.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container">
            {/* --- Header --- */}
            <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: '1rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span style={{ fontSize: '2rem' }}>✨</span>
                    <h2 style={{ margin: 0, background: 'var(--accent-gradient)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>Newgate Studio</h2>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.8rem', background: 'rgba(255,255,255,0.05)', padding: '5px 15px', borderRadius: '30px', border: '1px solid rgba(255,255,255,0.1)' }}>
                        {user.picture ? (
                            <img
                                src={user.picture}
                                alt="Profile"
                                referrerPolicy="no-referrer"
                                style={{ width: 32, height: 32, borderRadius: '50%', border: '2px solid #a855f7' }}
                            />
                        ) : (
                            <div style={{ width: 32, height: 32, borderRadius: '50%', background: '#6366f1' }} />
                        )}
                        <span style={{ fontSize: '0.9rem', color: '#f8fafc', fontWeight: 500 }}>{user.name?.split(' ')[0]}</span>
                    </div>
                    <button onClick={handleLogout} className="btn-logout" style={{ padding: '8px 16px', fontSize: '0.9rem' }}>
                        Logout
                    </button>
                </div>
            </header>

            {/* --- Main Workspace --- */}
            <div className="dashboard-grid">

                {/* LEFT: Controls Panel */}
                <div className="glass-card">
                    <h3 style={{ marginTop: 0, marginBottom: '1.5rem', fontSize: '1.2rem' }}>Configuration</h3>

                    {/* Prompt */}
                    <label style={{ display: 'block', marginBottom: '0.5rem', color: '#94a3b8', fontSize: '0.9rem' }}>Prompt</label>
                    <textarea
                        className="prompt-input"
                        rows="4"
                        placeholder="Describe your imagination..."
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                    />

                    {/* Uploads */}
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '2rem' }}>
                        {/* Self Image */}
                        <div>
                            <label style={{ display: 'block', marginBottom: '0.5rem', color: '#94a3b8', fontSize: '0.9rem' }}>Self Image</label>
                            <div className={`upload-box ${selfImage ? 'active' : ''}`} onClick={() => selfInputRef.current.click()}>
                                <input type="file" hidden ref={selfInputRef} onChange={(e) => handleFileChange(e, setSelfImage)} />
                                {selfImage ? (
                                    <img src={URL.createObjectURL(selfImage)} alt="Self" />
                                ) : (
                                    <>
                                        <span style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>👤</span>
                                        <span style={{ fontSize: '0.8rem' }}>Upload Self</span>
                                    </>
                                )}
                            </div>
                        </div>

                        {/* Target Image */}
                        <div>
                            <label style={{ display: 'block', marginBottom: '0.5rem', color: '#94a3b8', fontSize: '0.9rem' }}>Target Style</label>
                            <div className={`upload-box ${targetImage ? 'active' : ''}`} onClick={() => targetInputRef.current.click()}>
                                <input type="file" hidden ref={targetInputRef} onChange={(e) => handleFileChange(e, setTargetImage)} />
                                {targetImage ? (
                                    <img src={URL.createObjectURL(targetImage)} alt="Target" />
                                ) : (
                                    <>
                                        <span style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>🎨</span>
                                        <span style={{ fontSize: '0.8rem' }}>Upload Style</span>
                                    </>
                                )}
                            </div>
                        </div>
                    </div>

                    <button
                        className="btn-primary"
                        style={{ width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.5rem' }}
                        onClick={handleGenerate}
                        disabled={loading}
                    >
                        {loading ? 'Generating...' : '✨ Generate Magic'}
                    </button>
                </div>

                {/* RIGHT: Output Stage */}
                <div className="output-stage">
                    {outputImage ? (
                        <img
                            src={outputImage}
                            className="generated-image"
                            alt="Generated Output"
                            referrerPolicy="no-referrer"
                        />
                    ) : (
                        <div style={{ textAlign: 'center', color: 'rgba(255,255,255,0.2)' }}>
                            <div style={{ fontSize: '5rem', marginBottom: '1rem', filter: 'grayscale(100%) opacity(0.5)' }}>🖼️</div>
                            <p>Your masterpiece will appear here</p>
                        </div>
                    )}
                </div>
            </div>

            {/* --- Bottom: History --- */}
            <div style={{ marginTop: '3rem' }}>
                <h3 style={{ marginBottom: '1rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.5rem' }}>History</h3>

                {history.length === 0 ? (
                    <div style={{ padding: '2rem', textAlign: 'center', background: 'rgba(255,255,255,0.02)', borderRadius: '12px', color: '#64748b' }}>
                        No images generated yet. Start creating!
                    </div>
                ) : (
                    <div className="history-scroll">
                        {history.map((item) => (
                            <div
                                key={item.id}
                                className="history-item"
                                onClick={() => setOutputImage(item.generated_image_url || item.output_image_url)}
                                title={item.prompt}
                            >
                                {/* Image */}
                                {(item.generated_image_url || item.output_image_url) ? (
                                    <img
                                        src={item.generated_image_url || item.output_image_url}
                                        alt="Thumbnail"
                                        referrerPolicy="no-referrer"
                                    />
                                ) : (
                                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: '#94a3b8' }}>...</div>
                                )}

                                {/* Prompt Text Overlay */}
                                <div className="history-caption">
                                    {item.prompt}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default Dashboard;