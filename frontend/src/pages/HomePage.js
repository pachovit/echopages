import React from 'react';
import { Link } from 'react-router-dom';
import NavBar from '../components/NavBar';
import '../styles/HomePage.css';

const HomePage = () => {
    return (
        <div>
            <NavBar />
            <div className="home-content">
                {/* Hero Section */}
                <div className="hero-section">
                    <h1>EchoPages: Your Personalized Digest for Continuous Learning</h1>
                    <p>Delivering tailored summaries and insights to keep your knowledge journey alive.</p>
                    <Link to="/add-content" className="cta-button">Get Started for Free</Link>
                    <a href="https://github.com/pachovit/echopages" target="_blank" rel="noopener noreferrer" className="cta-button secondary">Learn More</a>
                </div>

                {/* What is EchoPages Section */}
                <section className="description-section">
                    <h2>What is EchoPages?</h2>
                    <p>
                        EchoPages is a unique service designed to help you retain and engage with content over time.
                        By curating personalized digests of your favorite books, articles, and more, EchoPages ensures
                        that learning and insight don’t just end after reading—they echo back to you, enhancing retention and deepening understanding.
                    </p>
                </section>

                {/* Features Section */}
                <section className="features">
                    <h2>Why EchoPages?</h2>
                    <ul>
                        <li><strong>Continuous Engagement:</strong> Never lose track of your progress. EchoPages sends you scheduled summaries, so your learning journey continues seamlessly.</li>
                        <li><strong>Personalized Content:</strong> Tailor your digests according to your interests. Whether it's a book, article, or a set of key quotes, EchoPages customizes content delivery based on your preferences.</li>
                        <li><strong>Self-Managed and Private:</strong> You are in full control. Manage your content, schedule delivery, and rest assured that your data stays private with our open-source platform.</li>
                        <li><strong>Free and Open Source:</strong> EchoPages is completely free to use. You can also self-host the service, giving you complete control over your data and usage.</li>
                    </ul>
                </section>

                {/* How It Works Section */}
                <section className="how-it-works">
                    <h2>How It Works</h2>
                    <div className="steps">
                        <div className="step">
                            <h3>1. Add Your Content</h3>
                            <p>Add summaries, quotes, or key points from your favorite books or articles into EchoPages. Our platform supports markdown and even images, making it easy to input and manage content.</p>
                        </div>
                        <div className="step">
                            <h3>2. Customize Your Schedule</h3>
                            <p>Decide when and how often you want to receive your digests. Whether daily, weekly, or custom, EchoPages adapts to your learning pace.</p>
                        </div>
                        <div className="step">
                            <h3>3. Receive and Review</h3>
                            <p>EchoPages will send your personalized digest directly to your inbox, helping you revisit and reinforce your learning material on your terms.</p>
                        </div>
                    </div>
                </section>

                {/* Testimonials Section */}
                <section className="testimonials">
                    <h2>What Users Are Saying</h2>
                    <div className="testimonial">
                        <p>“EchoPages transformed how I revisit my notes. The daily digests keep me engaged with the content long after I've read it.”</p>
                        <strong>- Sarah T., Writer</strong>
                    </div>
                    <div className="testimonial">
                        <p>“As a student, EchoPages has been invaluable for retaining key concepts from my textbooks.”</p>
                        <strong>- Michael R., Student</strong>
                    </div>
                    <div className="testimonial">
                        <p>“I love that I can control everything. It's my content, delivered my way.”</p>
                        <strong>- Laura D., Entrepreneur</strong>
                    </div>
                </section>

                {/* Call to Action Section */}
                <section className="call-to-action">
                    <h2>Get Started with EchoPages</h2>
                    <p>Ready to keep learning? Start using EchoPages today and experience a new way to engage with your favorite content. It's free, it's open-source, and it's tailored just for you.</p>
                    <Link to="/add-content" className="cta-button">Create Your First Digest</Link>
                </section>
            </div>
        </div>
    );
};

export default HomePage;