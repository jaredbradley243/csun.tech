/* eslint-disable react/self-closing-comp */
/* eslint-disable no-unused-vars */
/* eslint-disable prettier/prettier */
import React from 'react';
import { useParams } from 'react-router-dom';
import UserSidebar from '../components/UserSidebar';
import AccountSettings from '../components/AccountSettings';
import ChangePassword from '../components/ChangePassword';
import './UserProfile.css';
import Project from '../components/Project';

export default function UserProfile() {
    const { activepage } = useParams();

    return (
        <div className="container">
            <div className="userProfile">
                <div className="left">
                    <UserSidebar activepage={activepage} />
                </div>
                <div className="right">
                    {activepage === 'settings' && <AccountSettings />}
                    {activepage === 'project' && <Project />}
                    {activepage === 'change_password' && <ChangePassword />}
                </div>
            </div>
        </div>
    );
}
