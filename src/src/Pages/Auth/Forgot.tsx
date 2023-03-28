import { useState } from 'react';
import { LoadingOverlay, Paper, Title, Text, TextInput, Button, Container, Group, Anchor, Center, Box } from '@mantine/core';
import { IconArrowLeft } from '@tabler/icons';
import { useStore } from '../../store';
import { Link } from 'react-router-dom';
import { useStyles } from '../../styles';
import { useMutation } from '@apollo/client';
import { FORGOT_PASSWORD } from '../../graphql/mutations';
import { Error } from '../../Components/Error';


export function ForgotPasswordPage() {
  const { classes } = useStyles();
  const [email, setEmail] = useState("");
  let { user } = useStore();
  const [forgotPassword, forgotPasswordData] = useMutation(FORGOT_PASSWORD);

  const onChangeEmail = (e: any) => {
    setEmail(e.target.value);
  };

  const restore = () => {
    forgotPassword({
      variables: {
        form: {
          email: email
        }
      }
    });
  };

  return (
    <Container size={500} my={30}>
      <LoadingOverlay visible={user.isLoading} overlayBlur={2} />
      <Title className={classes.title} mb={"lg"} align="center">
        Forgot your password?
      </Title>
      {forgotPasswordData.data ? (
        <>
          <Text>We sent reset link to {email}. Please follow instructions.</Text>
        </>
      ) : (
        <>
          <Text color="dimmed" size="sm" align="center">
            Enter your email to get a reset link
          </Text>

          {!!forgotPasswordData.error && <Error text={forgotPasswordData.error.toString()} />}
          <Paper withBorder shadow="md" p={30} radius="md" mt="xl">
            <TextInput id="email" name={"email"} label="Your email" onChange={onChangeEmail} placeholder="Your email" required />
            <Group position="apart" mt="lg" className={classes.controls}>
              <Anchor color="dimmed" component={Link} to="/login" size="sm" className={classes.control}>
                <Center inline>
                  <IconArrowLeft size={12} stroke={1.5} />
                  <Box ml={5}>Back to login page</Box>
                </Center>
              </Anchor>
              <Button loading={forgotPasswordData.loading} className={classes.control} onClick={restore}>Reset password</Button>
            </Group>
          </Paper>
        </>
      )}
    </Container>
  );
}
