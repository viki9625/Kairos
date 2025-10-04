import React from 'react'

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className='bg-[#011c40] text-[#a7ebf2] py-4'>
        <p className='text-center'>Copyright &copy; {currentYear}  Kairos - Your wellness companion </p>
    </footer>
  )
}

export default Footer