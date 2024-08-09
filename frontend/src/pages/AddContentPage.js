import React from 'react';
import NavBar from '../components/NavBar';
import AddContentForm from '../components/AddContentForm';

const AddContentPage = () => {
    return (
        <div>
            <NavBar />
            <div className="page-content">
                <h1>Add New Content</h1>
                <AddContentForm />
            </div>
        </div>
    );
};

export default AddContentPage;