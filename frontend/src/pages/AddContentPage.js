import React from 'react';
import NavBar from '../components/NavBar';
import AddContentForm from '../components/AddContentForm';

const AddContentPage = () => {
    return (
        <div>
            <NavBar />
            <div className="page-content">
                <AddContentForm />
            </div>
        </div>
    );
};

export default AddContentPage;