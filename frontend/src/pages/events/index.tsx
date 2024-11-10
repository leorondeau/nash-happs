import { GetServerSideProps } from 'next';

interface Event {
  id: number;
  name: string;
  // Add more properties as needed
}

interface Props {
  events: Event[];
}

const MyPage = ({ events }: Props) => {
  // Use the events data in your component
  return (
    <div>
    <h1>Events</h1>
    <ul>
      {events.map((event) => (
        <li key={event.id}>{event.name}</li>
      ))}
    </ul>
  </div>
  );
};

// export const getServerSideProps: GetServerSideProps<Props> = async () => {
//   // Fetch data from the API endpoint
//   const res = await fetch('http://localhost:8000/events');
//   const events: Event[] = await res.json();

//   return {
//     props: { events },
//   };
// };

export const getServerSideProps: GetServerSideProps<Props> = async () => {
  // Simulate response data (replace this with your actual data)
  const mockEvents: Event[] = [
    { id: 1, name: 'Event 1' },
    { id: 2, name: 'Event 2' },
    // Add more mock events as needed
  ];

  return {
    props: { events: mockEvents },
  };
};

export default MyPage;