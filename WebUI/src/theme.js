import { createTheme } from '@mui/material/styles';
import { teal, orange } from '@mui/material/colors';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: teal[500], // Change the primary color to teal
    },
    secondary: {
      main: orange[500], // Change the secondary color to orange
    },
    background: {
      default: '#040D12', // Set a custom background color
      paper: '#040D12', // Set a custom paper color
    },
  },
});

export default theme;
