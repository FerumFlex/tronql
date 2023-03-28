import { useState } from 'react';
import { LoadingOverlay, Badge, TextInput, PasswordInput, Anchor, Paper, Title, Text, Container, Group, Button } from '@mantine/core';
import { Link, useNavigate } from 'react-router-dom';
import { useMutation } from '@apollo/client';
import { useStore } from '../../store';
import { observer } from 'mobx-react-lite';
import { Error } from '../../Components/Error';
import { LOGIN } from '../../graphql/mutations';
import { useStyles } from '../../styles';


export const LoginPage = observer(() => {
  const {classes} = useStyles();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const [login, loginData] = useMutation(LOGIN, {
    onCompleted(data: any) {
      localStorage.setItem("token", data.login.token.toString());
      localStorage.setItem("refreshToken", data.login.refreshToken.toString());
      user.setData(data.login.user);
      navigate("/dashboard");
    }
  });

  let { user } = useStore();

  const onChangeEmail = (e: any) => {
    setEmail(e.target.value);
  };

  const onChangePassword = (e: any) => {
    setPassword(e.target.value);
  };

  const signIn = () => {
    login({
      variables: {
        form: {
          email: email,
          password: password
        }
      }
    })
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
          <Title align="center" className={classes.title}>
            Welcome back!
          </Title>
          <Text color="dimmed" size="sm" align="center" mt={5}>
            Do not have an account yet?{' '}
            <Anchor component={Link} to="/register" size="sm">
              Create account
            </Anchor>
          </Text>

          {!!loginData.error && <Error text={loginData.error.toString()} /> }
          <Paper withBorder shadow="md" p={30} mt={30} radius="md">
            <TextInput label="Email" onChange={onChangeEmail} placeholder="Your email" required />
            <PasswordInput label="Password" onChange={onChangePassword} placeholder="Your password" required mt="md" />
            <Group position="apart" mt="lg">
              <Anchor component={Link} to="/forgot" size="sm">
                Forgot password?
              </Anchor>
            </Group>
            <Button loading={loginData.loading} onClick={signIn} fullWidth mt="xl">
              Sign in
            </Button>
          </Paper>
        </>
      )}
    </Container>
  );
});
