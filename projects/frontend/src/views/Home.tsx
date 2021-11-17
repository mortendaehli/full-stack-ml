import React, { FC, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';

import { getHealth } from '../utils/api';
import { isAuthenticated } from '../utils/auth';

const useStyles = makeStyles((theme) => ({
  link: {
    color: '#61dafb',
  },
}));

export const Home: FC = () => {
  const [message, setMessage] = useState<string>('');
  const [error, setError] = useState<string>('');
  const classes = useStyles();

  const queryBackend = async () => {
    try {
      const message = await getHealth();
      setMessage(message);
    } catch (err) {
      setError(String(err));
    }
  };

  return (
    <>
      <a className={classes.link} href="/admin">
        Admin Dashboard
      </a>
      <a className={classes.link} href="/protected">
        Protected Route
      </a>
      {isAuthenticated() ? (
        <a className={classes.link} href="/logout">
          Logout
        </a>
      ) : (
        <>
          <a className={classes.link} href="/login">
            Login
          </a>
          <a className={classes.link} href="/signup">
            Sign Up
          </a>
        </>
      )}
    </>
  );
};

export default Home;
