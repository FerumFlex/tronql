import { useState } from 'react';
import { LoadingOverlay, PasswordInput, Paper, Title, Text, Button, Container, Group, Anchor, Center, Box } from '@mantine/core';
import { IconArrowLeft } from '@tabler/icons';
import { useStore } from '../../store';
import { Link } from 'react-router-dom';
import { useStyles } from '../../styles';
import { useMutation } from '@apollo/client';
import { CHANGE_PASSWORD } from '../../graphql/mutations';
import { Error } from '../../Components/Error';
import { useParams } from 'react-router-dom';


export function ChangePasswordPage() {
  const {code} = useParams();
  const { classes } = useStyles();
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [error, setError] = useState("");
  let { user } = useStore();
  const [changePassword, changePasswordData] = useMutation(CHANGE_PASSWORD);

  const onChangePassword = (e: any) => {
    setPassword(e.target.value);
  };

  const onChangePassword2 = (e: any) => {
    setPassword2(e.target.value);
  };

  const restoreCode = () => {
    if (password !== password2) {
      setError("Password does not match");
      return;
    }
    changePassword({
      variables: {
        form: {
          changeId: code,
          password: password
        }
      }
    });
  };

  return (
    <Container size={500} my={30}>
      <LoadingOverlay visible={user.isLoading} overlayBlur={2} />
      <Title className={classes.title} align="center" mb={"lg"}>
        Forgot your password?
      </Title>
      { changePasswordData.data ? (
        <>
          <Text>You password was changes.</Text>
          <Text>Now you can <Anchor to={"/login"} component={Link}>login</Anchor> with new creds.</Text>
        </>
      ) : (
        <>
          <Text color="dimmed" size="sm" align="center">
            Enter code to confirm reset password
          </Text>

          {!!(error || changePasswordData.error) && <Error text={error || changePasswordData.error?.toString()} />}
          <Paper withBorder shadow="md" p={30} radius="md" mt="xl">
            <PasswordInput label="Password" onChange={onChangePassword} placeholder="Your new password" required mt="md" />
            <PasswordInput label="Password confirmation" onChange={onChangePassword2} placeholder="Your new password confirmation" required mt="md" />
            <Group position="apart" mt="lg" className={classes.controls}>
              <Anchor color="dimmed" component={Link} to="/login" size="sm" className={classes.control}>
                <Center inline>
                  <IconArrowLeft size={12} stroke={1.5} />
                  <Box ml={5}>Back to login page</Box>
                </Center>
              </Anchor>
              <Button loading={changePasswordData.loading} className={classes.control} onClick={restoreCode}>Reset password</Button>
            </Group>
          </Paper>
        </>
      )}
    </Container>
  );
}