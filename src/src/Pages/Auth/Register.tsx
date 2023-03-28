import { useState } from 'react';
import { LoadingOverlay, Badge, TextInput, PasswordInput, Anchor, Paper, Title, Text, Container, Group, Button } from '@mantine/core';
import { Link } from 'react-router-dom';
import { useMutation } from '@apollo/client';
import { SIGNUP } from '../../graphql/mutations';
import { Error } from '../../Components/Error';

import { useStore } from '../../store';
import { observer } from 'mobx-react-lite';
import { useStyles } from '../../styles';


export const RegisterPage = observer(() => {
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [signup, signupData] = useMutation(SIGNUP);
  const {classes} = useStyles();

  let { user } = useStore();

  const onChangeEmail = (e: any) => {
    setEmail(e.target.value);
  };

  const onChangePassword = (e: any) => {
    setPassword(e.target.value);
  };

  const register = () => {
    signup({
      variables: {
        form: {
          email: email,
          password: password
        }
      }
    });
  };

  const signOut = () => {
    user.logOut();
  }

  return (
    <Container size={500} my={40}>
      <LoadingOverlay visible={user.isLoading} overlayBlur={2} />
      {user.isLoggedIn ? (
          <Group>
          <Title size={"sm"}>You are logged in as <Badge>{user.props?.username}</Badge>:</Title>
          <Button onClick={signOut} size="sm">
            Logout
          </Button>
        </Group>
      ) : (
        <>
          {signupData.data ? (
            <>
              <Title className={classes.title} align="center">Email confirmation.</Title>
              <Text>We send email to {email}. Please confirm your account.</Text>
            </>
          ) : (
            <>
              <Title className={classes.title} align="center">
                Register new account
              </Title>
              <Text color="dimmed" size="sm" align="center" mt={5}>
                Do you have an account?{' '}
                <Anchor component={Link} to="/login" size="sm">
                  Login
                </Anchor>
              </Text>

              {!!signupData.error && <Error text={signupData.error.toString()} />}
              <Paper withBorder shadow="md" p={30} mt={30} radius="md">
                <TextInput name={"email"} type={"email"} label="Email" onChange={onChangeEmail} placeholder="Your email" required />
                <PasswordInput name={"password"} label="Password" onChange={onChangePassword} placeholder="Your password" required mt="md" />
                <Group position="apart" mt="lg">
                  <Anchor component={Link} to="/forgot" size="sm">
                    Forgot password?
                  </Anchor>
                </Group>
                <Button loading={signupData.loading} onClick={register} fullWidth mt="xl">
                  Register
                </Button>
              </Paper>
            </>
          )}
        </>
      )}
    </Container>
  );
});
