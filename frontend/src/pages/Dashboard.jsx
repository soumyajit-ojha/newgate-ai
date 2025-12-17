import React, { useState, useRef } from 'react';
import api from '../api';

const Dashboard = () => {
    const user = JSON.parse(localStorage.getItem('user') || '{}');

    // State for Inputs
    const [prompt, setPrompt] = useState('');
    const [selfImage, setSelfImage] = useState(null);
    const [targetImage, setTargetImage] = useState(null);

    // State for UI
    const [loading, setLoading] = useState(false);
    const [outputImage, setOutputImage] = useState(null);

    // File Input Refs (hidden inputs)
    const selfInputRef = useRef(null);
    const targetInputRef = useRef(null);

    // Mock History Data (We will connect API later)
    const [history] = useState([
        "https://picsum.photos/seed/101/200/200",
        "https://picsum.photos/seed/102/200/200",
        "https://picsum.photos/seed/103/200/200",
    ]);

    const handleLogout = () => {
        localStorage.clear();
        window.location.href = '/';
    };

    const handleFileChange = (e, setFile) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleGenerate = async () => {
        // 1. Validation
        if (!prompt) {
            alert("Please enter a prompt!");
            return;
        }
        if (!selfImage) {
            alert("Please upload your Self Image!");
            return;
        }
        if (!targetImage) {
            alert("Please upload a Target Style Image!");
            return;
        }

        setLoading(true);

        // 2. Prepare Data
        const formData = new FormData();
        formData.append('prompt', prompt);
        formData.append('self_image', selfImage);     // Must match backend param name
        formData.append('target_image', targetImage); // Must match backend param name

        try {
            // 3. Send to Backend
            const res = await api.post('/generate', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            // 4. Show Result
            setOutputImage(res.data.output_url);

        } catch (error) {
            console.error("Generation failed", error);
            alert("Something went wrong! Check console.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container">
            {/* --- Header --- */}
            <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <div className="flex items-center gap-2">
                    <span style={{ fontSize: '1.5rem' }}>✨</span>
                    <h2 style={{ margin: 0 }}>Newgate Studio</h2>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.8rem', background: 'rgba(255,255,255,0.05)', padding: '5px 15px', borderRadius: '30px' }}>
                        <div style={{ textAlign: 'right' }}>
                            <div style={{ fontSize: '0.9rem', fontWeight: '600' }}>{user.name}</div>
                            <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{user.email}</div>
                        </div>
                        {user.picture ? (
                            <img
                                src={user.picture}
                                alt="Profile"
                                style={{ width: 42, height: 42, borderRadius: '50%', border: '2px solid #a855f7' }}
                            />
                        ) : (
                            <div style={{ width: 42, height: 42, borderRadius: '50%', background: '#6366f1' }} />
                        )}
                    </div>
                    <button onClick={handleLogout} className="btn-logout" style={{ marginTop: 0, padding: '8px 16px', fontSize: '0.9rem' }}>
                        Logout
                    </button>
                </div>
            </header>

            {/* --- Main Workspace --- */}
            <div className="dashboard-grid">

                {/* LEFT: Controls */}
                <div className="glass-card" style={{ maxWidth: '100%', padding: '2rem', textAlign: 'left' }}>
                    <h3 style={{ marginTop: 0 }}>Create New Image</h3>

                    {/* 1. Prompt Input */}
                    <label style={{ display: 'block', marginBottom: '0.5rem', color: '#94a3b8' }}>Prompt</label>
                    <textarea
                        className="prompt-input"
                        rows="3"
                        placeholder="Describe what you want to see..."
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                    />

                    {/* 2. Image Uploads Grid */}
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '2rem' }}>

                        {/* Self Image Box */}
                        <div>
                            <label style={{ display: 'block', marginBottom: '0.5rem', color: '#94a3b8' }}>Self Image (You)</label>
                            <div
                                className={`upload-box ${selfImage ? 'active' : ''}`}
                                onClick={() => selfInputRef.current.click()}
                            >
                                <input
                                    type="file" hidden ref={selfInputRef}
                                    onChange={(e) => handleFileChange(e, setSelfImage)}
                                />
                                {selfImage ? (
                                    <div style={{ overflow: 'hidden', height: '100%', width: '100%' }}>
                                        <img src={URL.createObjectURL(selfImage)} style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: '8px' }} alt="Self" />
                                    </div>
                                ) : (
                                    <>
                                        <span style={{ fontSize: '1.5rem' }}>👤</span>
                                        <span>Upload Self</span>
                                    </>
                                )}
                            </div>
                        </div>

                        {/* Target Image Box */}
                        <div>
                            <label style={{ display: 'block', marginBottom: '0.5rem', color: '#94a3b8' }}>Target Style</label>
                            <div
                                className={`upload-box ${targetImage ? 'active' : ''}`}
                                onClick={() => targetInputRef.current.click()}
                            >
                                <input
                                    type="file" hidden ref={targetInputRef}
                                    onChange={(e) => handleFileChange(e, setTargetImage)}
                                />
                                {targetImage ? (
                                    <div style={{ overflow: 'hidden', height: '100%', width: '100%' }}>
                                        <img src={URL.createObjectURL(targetImage)} style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: '8px' }} alt="Target" />
                                    </div>
                                ) : (
                                    <>
                                        <span style={{ fontSize: '1.5rem' }}>🎨</span>
                                        <span>Upload Target</span>
                                    </>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Generate Button */}
                    <button
                        className="btn-primary"
                        style={{ width: '100%', padding: '1rem', fontSize: '1.1rem', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.5rem' }}
                        onClick={handleGenerate}
                        disabled={loading}
                    >
                        {loading ? (
                            <>Processing...</>
                        ) : (
                            <>✨ Generate Magic</>
                        )}
                    </button>
                </div>

                {/* RIGHT: Output Stage */}
                <div className="output-stage">
                    {outputImage ? (
                        <img src={outputImage} className="generated-image" alt="Generated Output" />
                    ) : (
                        <div style={{ textAlign: 'center', color: 'rgba(255,255,255,0.3)' }}>
                            <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>🖼️</div>
                            <p>Your masterpiece will appear here</p>
                        </div>
                    )}
                </div>
            </div>

            {/* --- Bottom: History --- */}
            <div style={{ marginTop: '3rem' }}>
                <h3 style={{ marginBottom: '1rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.5rem' }}>Recent Creations</h3>
                <div className="history-scroll">
                    {history.map((imgUrl, index) => (
                        <div key={index} className="history-item">
                            <img src={imgUrl} alt={`History ${index}`} />
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
